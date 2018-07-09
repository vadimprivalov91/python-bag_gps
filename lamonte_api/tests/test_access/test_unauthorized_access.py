__author__ = "Nikita Titov"
__copyright__ = "Copyright (c) 2015 Lamonte. All rights reserved."
__credits__ = ["Nikita Titov"]
__email__ = "nmtitov@nmtitov.com"

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UnauthorizedAccessTestCase(APITestCase):
    def test_login_allowed(self):
        response = self.client.post(reverse('rest_framework:login'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_allowed(self):
        response = self.client.post(reverse('rest_framework:logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_root_forbidden(self):
        response = self.client.get(reverse('v1:api-root'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bag_location_forbidden(self):
        response = self.client.get(reverse('bag_location'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bags_forbidden(self):
        response = self.client.get(reverse('v1:bag-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bags_unsafe_list_allowed(self):
        response = self.client.get(reverse('v1:bag-unsafe-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bag_detail_forbidden(self):
        response = self.client.get(reverse('v1:bag-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bag_tracking_forbidden(self):
        response = self.client.get(reverse('v1:bag-tracking', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bag_unsafe_bag_location_allowed(self):
        response = self.client.put(reverse('v1:bag-unsafe-bag-location', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
