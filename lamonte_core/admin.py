from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from lamonte_core.models import (
    LUser,
    Bag,
    Contact,
    DeviceDataEntry,
    LatestDeviceDataEntry
)
from datetime import datetime
# from math import isclose


class LUserChangeForm(UserChangeForm):
    pass


class BagInline(admin.StackedInline):
    model = Bag
    can_delete = True


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = LUser
        fields = ('name', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = LUser
        fields = ('name', 'email', 'lat', 'lon', 'password', 'is_active', 'is_admin', 'is_user_add_api_account', )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = (BagInline, )

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'email', 'is_admin', 'is_user_add_api_account', )
    list_filter = ('is_admin', 'is_admin', 'is_user_add_api_account', )
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Location', {'fields': ('lat', 'lon')}),
        ('Permissions', {'fields': ('is_admin', 'is_user_add_api_account', )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ('name', 'email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(LUser, MyUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


class ContactsInline(admin.StackedInline):
    model = Contact
    can_delete = True


@admin.register(Bag)
class BagAdmin(admin.ModelAdmin):
    inlines = (ContactsInline, )
    list_filter = ('owner__email', )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_filter = ('bag__owner__email', 'bag', )


@admin.register(DeviceDataEntry)
class DeviceDataEntryAdmin(admin.ModelAdmin):
    """
    List of fields
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
    search_fields = ('bag__owner__email', 'imei', 'data', )
    list_display = ('formatted_date', 'data_sent', 'imei', 'bag_url', 'altitude', 'google_maps_url', )
    list_filter = ('bag__owner__email', 'bag', 'imei', )
    readonly_fields = (
        'created', 'bag_url', 'imei', 'cell_id', 'timestamp',
        'lat', 'lon', 'google_maps_url',
        'altitude', 'speed', 'coarse', 'battery', 'temperature',
        'wifi_ssid_1', 'wifi_mac_id_1',
        'wifi_ssid_2', 'wifi_mac_id_2',
        'wifi_ssid_3', 'wifi_mac_id_3',
        'wifi_ssid_4', 'wifi_mac_id_4',
        'wifi_ssid_5', 'wifi_mac_id_5',
        'gsm_signal_strength', 'hdop',
        'num_of_satellite_used', 'gps_valid'

    )
    fields = (
        'created', 'bag_url', 'data', 'imei', 'cell_id', 'timestamp',
        'lat', 'lon', 'google_maps_url',
        'altitude', 'speed', 'coarse', 'battery', 'temperature',
        'wifi_ssid_1', 'wifi_mac_id_1',
        'wifi_ssid_2', 'wifi_mac_id_2',
        'wifi_ssid_3', 'wifi_mac_id_3',
        'wifi_ssid_4', 'wifi_mac_id_4',
        'wifi_ssid_5', 'wifi_mac_id_5',
        'gsm_signal_strength', 'hdop',
        'num_of_satellite_used', 'gps_valid'
    )

    def data_sent(self, obj):
        if obj.timestamp:
            return '%s GMT' % datetime.utcfromtimestamp(obj.timestamp).strftime("%b. %d, %Y, %H:%M:%S") if obj.created else None
        else:
            return 'Invalid time'
    data_sent.short_description = "data sent"
    data_sent.admin_order_field = 'timestamp'

    def formatted_date(self, obj):
        return '%s GMT' % obj.created.strftime("%b. %d, %Y, %H:%M:%S") if obj.created else None

    formatted_date.short_description = "Created"
    formatted_date.admin_order_field = 'created'

    def google_maps_url(self, instance):
        if instance.lat is None or instance.lon is None or isclose(instance.lat, 0) and isclose(instance.lon, 0):
            return mark_safe("<span class='errors'>Device didn't send GPS data</span>")
        data = {
            'base_url': 'http://maps.google.com/maps',
            'title': 'Google Maps URL',
            'lat': instance.lat,
            'lon': instance.lon,
        }
        format_string = '<a href="{base_url}?q={lat},{lon}" title="{title}" target="_blank" rel="noreferrer">{lat}, {lon}</a>'
        url_string = format_string.format(**data)
        return format_html(mark_safe(url_string))

    google_maps_url.short_description = "Location"
    google_maps_url.allow_tags = True

    def bag_url(self, instance):
        if instance.bag is None:
            return mark_safe("<span class='errors'>Bag record does not exist</span>")
        data = {
            'url': instance.bag.get_admin_url(),
            'title': instance.bag.name,
        }
        format_string = '<a href="{url}" title="{title}" target="_blank">{title}</a>'
        url_string = format_string.format(**data)
        return url_string

    bag_url.short_description = "Bag"
    bag_url.allow_tags = True





@admin.register(LatestDeviceDataEntry)
class LatestDeviceDataEntryAdmin(admin.ModelAdmin):
    search_fields = ('bag__owner__email', 'imei', 'data', )
    list_display = ('formatted_date', 'data_sent', 'imei', 'bag_url', 'altitude', 'google_maps_url', )
    list_filter = ('bag__owner__email', 'bag', 'imei', )
    readonly_fields = (
        'created', 'bag_url', 'imei', 'cell_id', 'timestamp',
        'lat', 'lon', 'google_maps_url',
        'altitude', 'speed', 'coarse', 'battery', 'temperature',
        'wifi_ssid_1', 'wifi_mac_id_1',
        'wifi_ssid_2', 'wifi_mac_id_2',
        'wifi_ssid_3', 'wifi_mac_id_3',
        'wifi_ssid_4', 'wifi_mac_id_4',
        'wifi_ssid_5', 'wifi_mac_id_5',
        'gsm_signal_strength', 'hdop',
        'num_of_satellite_used', 'gps_valid'

    )
    fields = (
        'created', 'bag_url', 'data', 'imei', 'cell_id', 'timestamp',
        'lat', 'lon', 'google_maps_url',
        'altitude', 'speed', 'coarse', 'battery', 'temperature',
        'wifi_ssid_1', 'wifi_mac_id_1',
        'wifi_ssid_2', 'wifi_mac_id_2',
        'wifi_ssid_3', 'wifi_mac_id_3',
        'wifi_ssid_4', 'wifi_mac_id_4',
        'wifi_ssid_5', 'wifi_mac_id_5',
        'gsm_signal_strength', 'hdop',
        'num_of_satellite_used', 'gps_valid'
    )

    def data_sent(self, obj):
        if obj.timestamp:
            return '%s GMT' % datetime.utcfromtimestamp(obj.timestamp).strftime("%b. %d, %Y, %H:%M:%S") if obj.created else None
        else:
            return 'Invalid time'
    data_sent.short_description = "data sent"
    data_sent.admin_order_field = 'timestamp'

    def formatted_date(self, obj):
        return '%s GMT' % obj.created.strftime("%b. %d, %Y, %H:%M:%S") if obj.created else None

    formatted_date.short_description = "Created"
    formatted_date.admin_order_field = 'created'

    def google_maps_url(self, instance):
        if instance.lat is None or instance.lon is None or isclose(instance.lat, 0) and isclose(instance.lon, 0):
            return mark_safe("<span class='errors'>Device didn't send GPS data</span>")
        data = {
            'base_url': 'http://maps.google.com/maps',
            'title': 'Google Maps URL',
            'lat': instance.lat,
            'lon': instance.lon,
        }
        format_string = '<a href="{base_url}?q={lat},{lon}" title="{title}" target="_blank" rel="noreferrer">{lat}, {lon}</a>'
        url_string = format_string.format(**data)
        return format_html(mark_safe(url_string))

    google_maps_url.short_description = "Location"
    google_maps_url.allow_tags = True

    def bag_url(self, instance):
        if instance.bag is None:
            return mark_safe("<span class='errors'>Bag record does not exist</span>")
        data = {
            'url': instance.bag.get_admin_url(),
            'title': instance.bag.name,
        }
        format_string = '<a href="{url}" title="{title}" target="_blank">{title}</a>'
        url_string = format_string.format(**data)
        return url_string

    bag_url.short_description = "Bag"
    bag_url.allow_tags = True

