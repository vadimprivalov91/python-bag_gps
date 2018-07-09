__author__ = "Nikita Titov"
__copyright__ = "Copyright (c) 2015 Lamonte. All rights reserved."
__credits__ = ["Nikita Titov"]
__email__ = "nmtitov@nmtitov.com"


from django.contrib.auth.models import Group
from rest_framework import serializers
from lamonte_core.models import (
    LUser,
    Bag,
    Contact,
    DeviceDataEntry,
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LUser
        fields = ('id', 'url', 'email', 'lat', 'lon', 'name')
        read_only_fields = ('url', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        name = validated_data.get('name',None)
        password = validated_data['password']
        user = self.Meta.model(
            email=email,
            name=name
        )
        user.set_password(password)
        user.save()
        return user


class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(required=False)
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_email(self, email):
        existing = LUser.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError("Someone with that email "
                "address has already registered.")

        return email

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                "confirm it.")

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")

        return data

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'iso', 'phone', 'e164Phone', 'formattedPhone', 'bag', )
        read_only_fields = ('id', 'bag', )


class BagSerializer(serializers.HyperlinkedModelSerializer):
    contacts = ContactSerializer(many=True, required=False)

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        bag = Bag.objects.create(**validated_data)
        for contact_data in contacts_data:
            Contact.objects.create(bag=bag, **contact_data)
        return bag

    def update(self, instance, validated_data):
        """
        Ignore provided contacts data
        """
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('imei', instance.imei)
        instance.macid = validated_data.get('macid', instance.macid)
        instance.geo_fence = validated_data.get('geo_fence', instance.geo_fence)
        instance.tracking = validated_data.get('tracking', instance.tracking)
        instance.save()
        return instance

    class Meta:
        model = Bag
        fields = ('id', 'name', 'imei', 'macid', 'altitude', 'geo_fence', 'tracking',
                  'lat', 'lon', 'image', 'nearby', 'distance', 'battery', 'charging', 'contacts', 'speed', )
        read_only_fields = ('altitude', 'nearby', 'distance', 'battery', 'charging', 'contacts', 'speed', )


class DeviceDataEntrySerializer(serializers.ModelSerializer):
    """
    Model fields
    created = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    imei = models.CharField(max_length=64, db_index=True, blank=True)
    timestamp = models.CharField(max_length=64, blank=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    coarse = models.FloatField(blank=True, null=True)
    cell_id = models.CharField(max_length=64, blank=True)
    battery = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    wifi_ssid_1 = models.CharField(max_length=32, blank=True)
    wifi_mac_id_1 = models.CharField(max_length=64, blank=True)
    wifi_ssid_2 = models.CharField(max_length=32, blank=True)
    wifi_mac_id_2 = models.CharField(max_length=64, blank=True)
    wifi_ssid_3 = models.CharField(max_length=32, blank=True)
    wifi_mac_id_3 = models.CharField(max_length=64, blank=True)
    wifi_ssid_4 = models.CharField(max_length=32, blank=True)
    wifi_mac_id_4 = models.CharField(max_length=64, blank=True)
    wifi_ssid_5 = models.CharField(max_length=32, blank=True)
    wifi_mac_id_5 = models.CharField(max_length=64, blank=True)
    gsm_signal_strength = models.CharField(max_length=64, blank=True, null=True)
    hdop = models.CharField(max_length=64, blank=True, null=True)
    num_of_satellite_used = models.CharField(max_length=64, blank=True, null=True)
    gps_valid = models.IntegerField(blank=True, null=True)
    """
    class Meta:
        model = DeviceDataEntry
        fields = (
            'id', 'created', 'data', 'imei', 'timestamp', 'lat', 'lon', 'speed', 'coarse',
            'cell_id', 'battery', 'altitude', 'temperature',
            'wifi_ssid_1', 'wifi_mac_id_1',
            'wifi_ssid_2', 'wifi_mac_id_2',
            'wifi_ssid_3', 'wifi_mac_id_3',
            'wifi_ssid_4', 'wifi_mac_id_4',
            'wifi_ssid_5', 'wifi_mac_id_5',
            'gsm_signal_strength', 'hdop',
            'num_of_satellite_used', 'gps_valid',
        )
        # everything except `data` is read only
        read_only_fields = (
            'id', 'created', 'imei', 'timestamp', 'lat', 'lon', 'speed', 'coarse',
            'cell_id', 'battery', 'altitude', 'temperature',
            'wifi_ssid_1', 'wifi_mac_id_1',
            'wifi_ssid_2', 'wifi_mac_id_2',
            'wifi_ssid_3', 'wifi_mac_id_3',
            'wifi_ssid_4', 'wifi_mac_id_4',
            'wifi_ssid_5', 'wifi_mac_id_5',
            'gsm_signal_strength', 'hdop',
            'num_of_satellite_used', 'gps_valid',
        )
