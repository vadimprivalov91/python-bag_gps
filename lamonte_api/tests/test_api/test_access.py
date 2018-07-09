__author__ = "Nikita Titov"
__copyright__ = "Copyright (c) 2015 Lamonte. All rights reserved."
__credits__ = ["Nikita Titov"]
__email__ = "nmtitov@nmtitov.com"


from jsonschema import validate, ValidationError
from lamonte_api.utils import random_email, random_string
from lamonte_core.models import LUser
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTestCase(APITestCase):
    email = None
    password = None
    user = None

    def setUp(self):
        self.email = random_email()
        self.password = random_string()
        self.user = LUser.objects.create(email=self.email)
        self.user.set_password(self.password)
        self.user.save()
        response = self.client.post('/api/api-token-auth/', {
            'username': self.email,
            'password': self.password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schema = {
            'type': 'object',
            'properties': {
                "token": {'type': 'string'},
            }
        }
        exception = False
        try:
            validate(response.data, schema)
        except ValidationError:
            exception = True
        self.assertFalse(exception)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

    def test_api_root_access_and_schema(self):
        response = self.client.get(reverse('v1:api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schema = {
            'type': 'object',
            'properties': {
                "device/apns": {'type': 'string'},
                "users": {'type': 'string'},
                "bags": {'type': 'string'},
            }
        }
        exception = False
        try:
            validate(response.data, schema)
        except ValidationError as e:
            exception = True
            raise e
        self.assertFalse(exception)

    def test_bag_list_access_and_schema(self):
        response = self.client.get(reverse('v1:bag-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schema = {
            'type': 'object',
            'properties': {
                "count": {'type': 'number'},
                "next": {'type': ['number', 'null']},
                "previous": {'type': ['number', 'null']},
                'results': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'email': {'type': 'string'},
                            'id': {'type': 'number'},
                            'lat': {'type': 'number'},
                            'lon': {'type': 'number'},
                            'url': {'type': 'string'},
                        }
                    }
                }
            }
        }
        exception = False
        try:
            validate(response.data, schema)
        except ValidationError as e:
            exception = True
            raise e
        self.assertFalse(exception)

    def test_device_data_entries_access_and_schema(self):
        response = self.client.get(reverse('v1:device_data_entries-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schema = {
            'type': 'object',
            'properties': {
                "count": {'type': 'number'},
                "next": {'type': ['number', 'null']},
                "previous": {'type': ['number', 'null']},
                'results': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'number'},
                            'created': {'type': 'string'},
                            'data': {'type': 'string'},
                        }
                    }
                }
            }
        }
        exception = False
        try:
            validate(response.data, schema)
        except ValidationError as e:
            exception = True
            raise e
        self.assertFalse(exception)
