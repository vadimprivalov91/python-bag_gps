from calendar import timegm
from django.utils import timezone


def timestamp():
    return timegm(timezone.now().utctimetuple())
