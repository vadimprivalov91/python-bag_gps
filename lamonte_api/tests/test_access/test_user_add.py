__author__ = "Nikita Titov"
__copyright__ = "Copyright (c) 2016 Lamonte. All rights reserved."
__credits__ = ["Nikita Titov"]
__email__ = "nmtitov@nmtitov.com"


from lamonte_api.utils import random_email, random_string
from lamonte_core.models import LUser
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserAddTestCase(APITestCase):

    def test_unauthorized_access_forbidden(self):
        response = self.client.post(reverse('v1:luser-add'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_access_forbidden(self):
        user = LUser.objects.create(email=random_email())
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse('v1:luser-add'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_add_api_user_can_create_users(self):
        user = LUser.objects.create(email=random_email())
        user.is_user_add_api_account = True
        user.save()
        self.client.force_authenticate(user=user)

        email = random_email()
        response = self.client.post(reverse('v1:luser-add'), data={'email': email, 'password': random_string()})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertEqual(data['email'], email)

        try:
            user = LUser.objects.get(email=email)
            self.assertIsNotNone(user)
        except LUser.DoesNotExist as e:
            self.assertFalse(True, e.message)

    def test_superuser_can_create_users(self):
        superuser = LUser.objects.create_superuser(email=random_email(), password=random_string())
        self.client.force_authenticate(user=superuser)

        email = random_email()
        response = self.client.post(reverse('v1:luser-add'), data={'email': email, 'password': random_string()})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data
        self.assertEqual(data['email'], email)

        try:
            user = LUser.objects.get(email=email)
            self.assertIsNotNone(user)
        except LUser.DoesNotExist as e:
            self.assertFalse(True, e.message)

    def test_superuser_cant_create_user_without_password(self):
        user = LUser.objects.create_superuser(email=random_email(), password=random_string())
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse('v1:luser-add'), data={'email': random_email()})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_cant_create_user_without_username(self):
        user = LUser.objects.create_superuser(email=random_email(), password=random_string())
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse('v1:luser-add'), data={'password': random_string()})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superuser_cant_create_user_without_username_and_password(self):
        user = LUser.objects.create_superuser(email=random_email(), password=random_string())
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse('v1:luser-add'), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)