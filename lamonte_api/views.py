__author__ = "Nikita Titov"
__copyright__ = "Copyright (c) 2015 Lamonte. All rights reserved."
__credits__ = ["Nikita Titov"]
__email__ = "nmtitov@nmtitov.com"


from django.contrib.auth.models import Group
from django.db.models import Q
from django.db import transaction
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import (
    APIException, AuthenticationFailed, NotFound, PermissionDenied
    )
from rest_framework import permissions
from rest_framework.response import Response
from lamonte_api.serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    BagSerializer,
    ContactSerializer,
    DeviceDataEntrySerializer,
)
from lamonte_core.models import (
    LUser,
    Bag,
    Contact,
    DeviceDataEntry,
    LatestDeviceDataEntry
)
from lamonte_api.permissions import IsAnonymousPostOrAuthenticated, IsAnonymousBagSensorOrAuthenticated, IsOwner, IsUsersAddAPIUser
from lamonte_api.negotiation import MyContentNegotiation
import logging
from rest_framework.authtoken.models import Token
from lamonte_core.math import isclose

class ClientError(APIException):
    status_code = 400
    default_detail = 'Client error'


class AuthorizationError(APIException):
    status_code = 403
    default_detail = 'Authorization error'


class UserLocationView(views.APIView):

    def post(self, request):
        try:
            lat = request.data["lat"]
            lon = request.data["lon"]
            user = request.user
            user.lat = lat
            user.lon = lon
            user.update_distance()
            user.save()
            return Response(status=status.HTTP_200_OK)
        except KeyError:
            raise ClientError(detail='Latitude and longitude are required')


class BagLocationView(views.APIView):

    def post(self, request):
	#print ("testttttttttttttttttttttttt")
        try:
            imei = request.data["code"]
            lat = float(request.data["lat"])
            lon = float(request.data["lon"])
            geo_fence = float(request.data["geo_fence"])
            altitude = request.data.get("altitude",None)
            altitude = None if altitude == '' else altitude
            if altitude:
                altitude = float(altitude)
            battery = request.data.get("battery",None)
            battery = None if battery == '' else battery

            bag = Bag.objects.get(imei=imei)
            if not (lat is None or lon is None or isclose(lat, 0) and isclose(lon, 0)):
                bag.lat = lat
                bag.lon = lon
                bag.update_distance()
            if altitude is not None and not isclose(altitude, 0):
                bag.altitude = altitude
            if battery is not None:
                battery = float(battery)/100.0
                bag.battery = battery
            bag.geo_fence = float(geo_fence)
            bag.update_distance()
            bag.save()
            device_entries = DeviceDataEntry(imei=imei,bag=bag,altitude=altitude,battery=battery,lat=lat,lon=lon)
            device_entries.save(from_app=True)
            return Response({"message":"SUCCESS"},status=status.HTTP_200_OK)
        except KeyError:
            raise ClientError(detail='code, latitude, longitude and geo_fence are required')
        except Bag.DoesNotExist:
            raise NotFound(detail='Bag does not exist')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = LUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAnonymousPostOrAuthenticated, )

    @list_route(methods=['GET'], permission_classes=[permissions.AllowAny])
    def lookup(self, request):
        auth = TokenAuthentication()
        try:
            key = request.query_params['key']
            user, key = auth.authenticate_credentials(key)
            user_serializer = self.serializer_class(user, context={'request': request})
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'key': ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed:
            raise NotFound(detail="User doesn't exist")

    @list_route(methods=['POST'], permission_classes=[IsUsersAddAPIUser])
    def add(self, request):
        try:
            email = request.data["email"]
            name = request.data.get("name",None)
            password = request.data["password"]
            user = LUser.objects.filter(email=email)
            if user.exists():
                format_string = 'User with email {email} already exists'
                data = {'email': email}
                string = format_string.format(**data)
                raise ClientError(detail=string)
            created_user = LUser.objects.create_user(email, name, password)

            serializer = self.serializer_class(created_user, context={'request': request})
            return Response(serializer.data, status=201)
        except Exception as e:
            raise ClientError(detail=e)

    @list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        # Validating our serializer from the UserRegistrationSerializer
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.data.get('name',None)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        created_user = LUser.objects.create_user(email, name, password)

        serializer = self.serializer_class(created_user, context={'request': request})
        data = serializer.data
        if Token.objects.filter(user=created_user).exists():
            data['token'] = Token.objects.get(user=created_user).key

        return Response(data, status=201)


class BagViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAnonymousBagSensorOrAuthenticated, )
    """
    API endpoint that allows bags to be viewed or edited.
    """
    serializer_class = BagSerializer
    

    def get_queryset(self):
        return Bag.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @list_route(methods=['get'])
    def unsafe_list(self, request):
        xs = Bag.objects.all()
        xs = self.serializer_class(xs, many=True, context={'request': request})
        return Response({"results": xs.data}, status=status.HTTP_200_OK)

    @detail_route(methods=['put'])
    def tracking(self, request, pk=None):
        try:
            tracking = request.data["tracking"]
            bag = self.get_object()
            bag.tracking = tracking
            bag.save()
            serializer = self.serializer_class(bag, context={'request': request})
            return Response({"results": serializer.data}, status=200)
        except KeyError:
            raise ClientError(detail='Tracking required')
        except Bag.DoesNotExist:
            raise NotFound(detail='Bag does not exist or code is wrong')


class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsOwner, )
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        user = self.request.user
        item_pk = self.kwargs['bag_pk']
        try:
            item = Bag.objects.get(id=item_pk, owner=user)
            name = self.request.data['name']
            iso = self.request.data['iso']
            phone = self.request.data['phone']
            e164_phone = self.request.data['e164Phone']
            formatted_phone = self.request.data['formattedPhone']
            contact = serializer.save(bag=item, name=name, iso=iso, phone=phone, e164Phone=e164_phone,
                                      formattedPhone=formatted_phone)
        except Bag.DoesNotExist:
            NotFound(detail="Bag does not exist")

    def get_queryset(self):
        user = self.request.user
        bag_pk = self.kwargs['bag_pk']
        return Contact.objects.filter(bag_id=bag_pk)


logger = logging.getLogger('django.request')


class DeviceDataEntryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    """
    API endpoint that allows get and post data entries (keep it alive).
    http -f http://lamonte-london.com/api/v1/device_data_entries/ data=hello

    data is comma-separated string
    <IMEI>,<Time Stamp>,<+/-Latitude>,<+/-Longitude>,<Speed>,
    <Coarse>,<Cell Id>,<Battery status>,<Altitude>,<Temperature>,
    <WIFI-SSID-1>,< WIFI-MAC-ID-1>,< WIFI-SSID-2>,< WIFI-MAC-ID-2>,< WIFI-SSID-3>,< WIFI-MAC-ID-3>,< WIFI-SSID-4>,< WIFI-MAC-ID-4>,< WIFI-SSID-5>,< WIFI-MAC-ID-5>
    """
    serializer_class = DeviceDataEntrySerializer

    def get_queryset(self):
        return DeviceDataEntry.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        response = super(DeviceDataEntryViewSet, self).create(request, *args, **kwargs)
        logger.info(str(request.stream))
        logger.info(str(request.data))
        response.data = {"message": "SUCCESS"}  # remove response body to save energy of the device
        return response


class LatestDeviceDataEntryView(views.APIView):

    def get(self, request, imei):
        try:
            bag = Bag.objects.get(imei=imei)
            if not request.user.bag_set.filter(id=bag.id).exists():
                raise PermissionDenied(detail="You don't have permission to access the requested bag details")
            data = bag.to_dict()
            data['last_updated_time']  = None
            if LatestDeviceDataEntry.objects.filter(bag=bag).exists():
                latest_data = LatestDeviceDataEntry.objects.get(bag=bag)
                data['last_updated_time'] = latest_data.created
            return Response(data, status=status.HTTP_200_OK)
        except Bag.DoesNotExist:
            raise NotFound(detail='Bag does not exist or code is wrong')
