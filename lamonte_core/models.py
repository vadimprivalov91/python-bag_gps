from __future__ import print_function, division, absolute_import
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from geopy.distance import vincenty as geo_distance
from geopy.geocoders import Nominatim
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from lamonte_core.csv import CommaSeparatedValues
from lamonte_core.files import slugify_filename
from lamonte_core.sms import send_sms
from lamonte_core.math import isclose
from lamonte_core.time import timestamp
from os import path as op
from push_notifications.models import APNSDevice
import json
import lamonte_core.redis_client
import logging
import math
from django.forms import model_to_dict
import datetime
from rest_framework.authtoken.models import Token

logger = logging.getLogger('django.request')


class CoordinateMixin(object):

    @property
    def coordinate(self):
        return self.lat, self.lon


def image_path(bag, filename):
    name, ext = op.splitext(filename)
    name = str(timestamp())
    filename = name + ext
    user_dir = 'user_%s' % bag.owner_id
    return op.join('bags', user_dir, slugify_filename(filename))


class LUserManager(BaseUserManager):
    def create_user(self, email, name=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name = name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class LUser(AbstractBaseUser, CoordinateMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=256, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_user_add_api_account = models.BooleanField(default=False)

    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = LUserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.name

    def __unicode__(self):
        return self.name if self.name else self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.name if self.name else self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_superuser(self):
        "Is the user a member of superusers?"
        # Simplest possible answer: All admins are superusers
        return self.is_admin

    def notify(self, message):
        devices = APNSDevice.objects.filter(user=self)
        if not devices:
            return
        devices.send_message(message, sound='default')

    def update_distance(self):
        for bag in self.bag_set.all():
            bag.update_distance()
            bag.save()
            bag.publish_bag_move()

    def save(self, *args, **kwargs):
        super(LUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'User'
        verbose_name_plural = u'Users'


class BagNotificationDelegate(object):

    def bag_did_move(self, bag):
        bag.publish_bag_move()
        print("Bag %s did move" % bag.name)

    def bag_did_move_away(self, bag):
        # Reverse geocoding is disabled due to timeout issues.
        # This procedure must be moved to background thread.
        #
        # geolocator = Nominatim()
        # location = geolocator.reverse((bag.lat, bag.lon))
        # message = "%s is out of geo fence! Last seen: %s" % (bag.name, location.address)
        message = "%s is out of geo fence!" % bag.name
        # sms
        for contact in bag.contacts.all():
            send_sms(contact.e164Phone, message)
        # apns
        bag.owner.notify(message)
        # redis
        bag.publish_bag_away()
        print("Bag %s did move away" % bag.name)

    def bag_did_come_near(self, bag):
        bag.publish_bag_near()
        print("Bag %s did come near" % bag.name)


BAG_MOVE = 'bag_move'
BAG_NEAR = 'bag_near'
BAG_AWAY = 'bag_away'


class Bag(models.Model, CoordinateMixin):
    owner = models.ForeignKey(LUser)
    name = models.CharField(max_length=1024, db_index=True)
    imei = models.BigIntegerField(verbose_name='IMEI', unique=True)
    geo_fence = models.FloatField(default=10)  # ft
    tracking = models.BooleanField(default=True, db_index=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    altitude = models.FloatField(null=True, blank=True)
    speed = models.FloatField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)
    nearby = models.BooleanField(default=False, db_index=True)
    battery = models.FloatField(default=1, validators=[MinValueValidator(0), MaxValueValidator(1)])
    charging = models.BooleanField(default=False)
    image = ProcessedImageField(blank=True, null=True, upload_to=image_path,
                                processors=[ResizeToFit(100 * 4, 100 * 4)],
                                format='JPEG', options={})
    macid = models.CharField(max_length=250, unique=True, null=True, blank=True)

    def get_admin_url(self):
        relative_url = reverse("admin:lamonte_core_bag_change", args=(self.pk, ))
        return ''.join(['http://', 'lamonte-london.com', relative_url])

    delegate = BagNotificationDelegate()

    def update_distance(self):
        self.distance = geo_distance(self.coordinate, self.owner.coordinate).feet
        if self.nearby:
            if self.distance > self.geo_fence:
                self.nearby = False
                self.delegate.bag_did_move_away(self)
        else:
            if self.distance < self.geo_fence:
                self.nearby = True
                self.delegate.bag_did_come_near(self)

    def save(self, *args, **kwargs):
        super(Bag, self).save(*args, **kwargs)

    def publish_bag_move(self):
        lamonte_core.redis_client.redis_client.publish(BAG_MOVE, self.to_json())

    def publish_bag_near(self):
        lamonte_core.redis_client.redis_client.publish(BAG_NEAR, self.to_json())

    def publish_bag_away(self):
        lamonte_core.redis_client.redis_client.publish(BAG_AWAY, self.to_json())

    def to_dict(self):
        return {
            'owner_id': self.owner_id,
            'id': self.id,
            'lat': self.lat,
            'lon': self.lon,
            'distance': self.distance,
            'battery': self.battery,
            'charging': self.charging,
            'tracking':self.tracking,
            'macid':self.macid
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']
        verbose_name = u'Bag'
        verbose_name_plural = u'Bags'


class Contact(models.Model):
    bag = models.ForeignKey(Bag, related_name='contacts')
    name = models.CharField(max_length=1024, db_index=True)
    iso = models.CharField(max_length=3)
    phone = models.CharField(max_length=1024)
    e164Phone = models.CharField(max_length=1024)
    formattedPhone = models.CharField(max_length=1024)

    def to_dict(self):
        return {
            'bag_id': self.owner_id,
            'name': self.name,
            'iso': self.iso,
            'phone': self.phone,
            'e164Phone': self.e164Phone,
            'formattedPhone': self.formattedPhone,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = u'Contact Assigned for Bag'
        verbose_name_plural = u'Contacts Assigned for Bag'


class LatestDeviceDataEntry(models.Model):
    """
    data is comma-separated string
    <IMEI>,<Time Stamp>,<+/-Latitude>,<+/-Longitude>,<Speed>,
    <Coarse>,<Cell Id>,<Battery status>,<Altitude>,<Temperature>,
    <WIFI-SSID-1>,< WIFI-MAC-ID-1>,< WIFI-SSID-2>,< WIFI-MAC-ID-2>,< WIFI-SSID-3>,< WIFI-MAC-ID-3>,< WIFI-SSID-4>,< WIFI-MAC-ID-4>,< WIFI-SSID-5>,< WIFI-MAC-ID-5>,
    <GSM Signal Strength>,<HDOP>,<Number of Satellite used for fix>,<GPS Valid>
    """
    created = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    imei = models.BigIntegerField(db_index=True, blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    coarse = models.FloatField(blank=True, null=True)
    cell_id = models.IntegerField(blank=True, null=True)
    battery = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    wifi_ssid_1 = models.CharField(max_length=32, blank=True)
    wifi_ssid_2 = models.CharField(max_length=32, blank=True)
    wifi_ssid_3 = models.CharField(max_length=32, blank=True)
    wifi_ssid_4 = models.CharField(max_length=32, blank=True)
    wifi_ssid_5 = models.CharField(max_length=32, blank=True)
    wifi_mac_id_1 = models.CharField(max_length=64, blank=True)
    wifi_mac_id_2 = models.CharField(max_length=64, blank=True)
    wifi_mac_id_3 = models.CharField(max_length=64, blank=True)
    wifi_mac_id_4 = models.CharField(max_length=64, blank=True)
    wifi_mac_id_5 = models.CharField(max_length=64, blank=True)
    gsm_signal_strength = models.CharField(max_length=64, blank=True, null=True)
    hdop = models.CharField(max_length=64, blank=True, null=True)
    num_of_satellite_used = models.CharField(max_length=64, blank=True, null=True, verbose_name="Number of satellite used for fix")
    gps_valid = models.IntegerField(blank=True, null=True)

    bag = models.ForeignKey(Bag, related_name='device_data_entry', blank=True, null=True)

    def __str__(self):
        """
        coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
        'Coordinates: {latitude}, {longitude}'.format(**coord)
        """
        data = {
            'created': self.created.strftime("%A, %d. %B %Y %H:%M:%S"),
            'imei': self.imei,
            'lat': self.lat,
            'lon': self.lon,
            'altitude': self.altitude,
        }
        format_string = "{created} imei {imei}, location ({lat}, {lon}), altitude {altitude} feet"
        description = format_string.format(**data)
        return description

    class Meta:
        ordering = ['-created']
        verbose_name = u'Latest Device Data Entry'
        verbose_name_plural = u'Latest Device Data Entries'


class DeviceDataEntry(models.Model):
    """
    data is comma-separated string
    <IMEI>,<Time Stamp>,<+/-Latitude>,<+/-Longitude>,<Speed>,
    <Coarse>,<Cell Id>,<Battery status>,<Altitude>,<Temperature>,
    <WIFI-SSID-1>,< WIFI-MAC-ID-1>,< WIFI-SSID-2>,< WIFI-MAC-ID-2>,< WIFI-SSID-3>,< WIFI-MAC-ID-3>,< WIFI-SSID-4>,< WIFI-MAC-ID-4>,< WIFI-SSID-5>,< WIFI-MAC-ID-5>,
    <GSM Signal Strength>,<HDOP>,<Number of Satellite used for fix>,<GPS Valid>
    """
    created = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    imei = models.BigIntegerField(db_index=True, blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    coarse = models.FloatField(blank=True, null=True)
    cell_id = models.IntegerField(blank=True, null=True)
    battery = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    wifi_ssid_1 = models.CharField(max_length=32, blank=True)
    wifi_ssid_2 = models.CharField(max_length=32, blank=True)
    wifi_ssid_3 = models.CharField(max_length=32, blank=True)
    wifi_ssid_4 = models.CharField(max_length=32, blank=True)
    wifi_ssid_5 = models.CharField(max_length=32, blank=True)
    wifi_mac_id_1 = models.CharField(max_length=64, blank=True)
    wifi_mac_id_2 = models.CharField(max_length=64, blank=True)
    wifi_mac_id_3 = models.CharField(max_length=64, blank=True)
    wifi_mac_id_4 = models.CharField(max_length=64, blank=True)
    wifi_mac_id_5 = models.CharField(max_length=64, blank=True)
    gsm_signal_strength = models.CharField(max_length=64, blank=True, null=True)
    hdop = models.CharField(max_length=64, blank=True, null=True)
    num_of_satellite_used = models.CharField(max_length=64, blank=True, null=True, verbose_name="Number of satellite used for fix")
    gps_valid = models.IntegerField(blank=True, null=True)

    bag = models.ForeignKey(Bag, related_name='device_data_entries', blank=True, null=True)

    def save(self, *args, **kwargs):
        if 'from_app' in kwargs:
            del kwargs['from_app']
            super(DeviceDataEntry, self).save(*args, **kwargs)
        else:
            try:
                # parse data
                csv = CommaSeparatedValues(self.data)
                self.imei = csv.get(0, 0)
                self.timestamp = math.trunc(csv.get(1, 0.0))
                self.lat = csv.get(2, 0.0)
                self.lon = csv.get(3, 0.0)
                self.speed = csv.get(4, 0.0)
                self.coarse = csv.get(5, 0.0)
                self.cell_id = csv.get(6, 0)
                self.battery = csv.get(7, 0.0)
                self.altitude = csv.get(8, 0.0)
                self.temperature = csv.get(9, 0.0)
                self.wifi_ssid_1 = csv.get(10, "")
                self.wifi_mac_id_1 = csv.get(11, "")
                self.wifi_ssid_2 = csv.get(12, "")
                self.wifi_mac_id_2 = csv.get(13, "")
                self.wifi_ssid_3 = csv.get(14, "")
                self.wifi_mac_id_3 = csv.get(15, "")
                self.wifi_ssid_4 = csv.get(16, "")
                self.wifi_mac_id_4 = csv.get(17, "")
                self.wifi_ssid_5 = csv.get(18, "")
                self.wifi_mac_id_5 = csv.get(19, "")
                self.gsm_signal_strength = csv.get(20, "")
                self.hdop = csv.get(21, "")
                self.num_of_satellite_used = csv.get(22, "")
                gps_valid = csv.get(23, "")
                #'1' Present Location. '0'  Last know location (If available)
                self.gps_valid = int(gps_valid.replace("'","")) if gps_valid else None
                gps_valid_no = int(gps_valid.replace("'","")) if gps_valid else None

                # update bag
                bag = Bag.objects.get(imei=csv.get(0, 0))

                if not (self.lat is None or self.lon is None or isclose(self.lat, 0) and isclose(self.lon, 0)):
                    bag.lat = self.lat
                    bag.lon = self.lon
                    bag.update_distance()

                if not isclose(self.altitude, 0):
                    bag.altitude = self.altitude

                bag.speed = self.speed

                bag.battery = self.battery / 100.0
                bag.save()
                self.bag = bag
                if (datetime.datetime.now() - self.created).seconds >= 15:
                    bag.publish_bag_move()
                    
            except (KeyError, Bag.DoesNotExist, Exception) as e:
                logger.error(str(e))
            super(DeviceDataEntry, self).save(*args, **kwargs)

        self.update_latest_entry()

    def update_latest_entry(self):
        data = model_to_dict(self, exclude=['imei', 'bag'])
        try:
            bag = Bag.objects.get(imei=self.imei)
            data['bag'] = bag
            data['created'] = self.created
            latest, created = LatestDeviceDataEntry.objects.get_or_create(imei=self.imei, defaults=data)
            if not created:
                LatestDeviceDataEntry.objects.filter(imei=self.imei).update(**data)
        except Exception as e:
            latest, created = LatestDeviceDataEntry.objects.get_or_create(imei=self.imei, defaults=data)
            if not created:
                LatestDeviceDataEntry.objects.filter(imei=self.imei).update(**data)
  
    def to_dict(self):
        return {
            'created': self.created,
            'data': self.data,
        }

    def __str__(self):
        """
        coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
        'Coordinates: {latitude}, {longitude}'.format(**coord)
        """
        data = {
            'created': self.created.strftime("%A, %d. %B %Y %H:%M:%S"),
            'imei': self.imei,
            'lat': self.lat,
            'lon': self.lon,
            'altitude': self.altitude,
        }
        format_string = "{created} imei {imei}, location ({lat}, {lon}), altitude {altitude} feet"
        description = format_string.format(**data)
        return description

    class Meta:
        ordering = ['-created']
        verbose_name = u'Device Data Entry'
        verbose_name_plural = u'Device Data Entries'




@receiver(post_save, sender=LUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
