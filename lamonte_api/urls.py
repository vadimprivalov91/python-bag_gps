__author__ = "Nikita Titov"
__copyright__ = "Copyright (c) 2015 Lamonte. All rights reserved."
__credits__ = ["Nikita Titov"]
__email__ = "nmtitov@nmtitov.com"

from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework.authtoken import views as token_views
from lamonte_api import views
from lamonte_api.drf_apn_views import APNSDeviceViewSet


router = routers.DefaultRouter()
router.register(r'device/apns', APNSDeviceViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'bags', views.BagViewSet, base_name='bag')
router.register(r'device_data_entries', views.DeviceDataEntryViewSet, base_name='device_data_entries')
contacts_router = NestedSimpleRouter(router, r'bags', lookup='bag')
contacts_router.register(r'contacts', views.ContactViewSet, base_name='contact')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^v1/', include(router.urls, namespace='v1')),
    url(r'^v1/', include(contacts_router.urls, namespace='v1')),
    url(r'^v1/user_location/$', views.UserLocationView.as_view(), name='user_location'),
    url(r'^v1/bag_location/$', views.BagLocationView.as_view(), name='bag_location'),
 	url(r'^v1/(?P<imei>\d+)/latest_data_entries/$', views.LatestDeviceDataEntryView.as_view(), name='lastest_data_entry'),

    # url(r'^v1/', include(lists_router.urls, namespace='v1')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', token_views.obtain_auth_token)
]
