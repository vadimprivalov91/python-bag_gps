__author__ = "Nikita Titov"
__copyright__ = "Copyright (c) 2015 Lamonte. All rights reserved."
__credits__ = ["Nikita Titov"]
__email__ = "nmtitov@nmtitov.com"


from django.test import TestCase
from lamonte_core.models import (
    Bag,
    Contact,
    LUser,
)


class ModelsDescriptionsTestCase(TestCase):
    def test_user(self):
        email = "test@test.com"
        user = LUser.objects.create(email=email)
        self.assertEqual(str(user), email)

    def test_bag(self):
        user = LUser.objects.create(email="test@test.com")
        name = "Test bag"
        imei = 356938035643809
        bag = Bag.objects.create(name=name, imei=imei, owner=user)
        self.assertEqual(str(bag), name)

    def test_contact(self):
        user = LUser.objects.create(email="test@test.com")
        name = "Test bag"
        imei = 356938035643809
        bag = Bag.objects.create(name=name, imei=imei, owner=user)
        name = "Bodyguard"
        phone = "+12012340001"
        contact = Contact.objects.create(name=name, phone=phone, e164Phone=phone, formattedPhone=phone, bag=bag)
        self.assertEqual(str(contact), name)
