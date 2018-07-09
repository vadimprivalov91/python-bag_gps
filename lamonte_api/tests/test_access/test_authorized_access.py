__author__ = "Nikita Titov"
__copyright__ = "Copyright (c) 2015 Lamonte. All rights reserved."
__credits__ = ["Nikita Titov"]
__email__ = "nmtitov@nmtitov.com"


from lamonte_api.utils import random_email
from lamonte_core.models import LUser
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthorizedAccessTestCase(APITestCase):
    user = None

    def setUp(self):
        self.user = LUser.objects.create(email=random_email())
        self.client.force_authenticate(user=self.user)

    def test_api_root_allowed(self):
        response = self.client.get(reverse('v1:api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bag_location_allowed(self):
        response = self.client.post(reverse('bag_location'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bags_allowed(self):
        response = self.client.get(reverse('v1:bag-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bags_unsafe_list_allowed(self):
        response = self.client.get(reverse('v1:bag-unsafe-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bag_detail_allowed(self):
        response = self.client.get(reverse('v1:bag-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bag_tracking_allowed(self):
        response = self.client.put(reverse('v1:bag-tracking', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bag_unsafe_bag_location_allowed(self):
        response = self.client.put(reverse('v1:bag-unsafe-bag-location', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
