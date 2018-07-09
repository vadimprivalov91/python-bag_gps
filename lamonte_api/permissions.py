__author__ = "Nikita Titov"
__copyright__ = "Copyright (c) 2015 Lamonte. All rights reserved."
__credits__ = ["Nikita Titov"]
__email__ = "nmtitov@nmtitov.com"

from rest_framework import permissions
from lamonte_core.models import Contact


class IsAnonymousPostOrAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(IsAnonymousPostOrAuthenticated, self).has_permission(request, view)


class IsAnonymousBagSensorOrAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if view.action and view.action.startswith('unsafe_'):
            return True
        return super(IsAnonymousBagSensorOrAuthenticated, self).has_permission(request, view)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif isinstance(obj, Contact):
            return obj.bag.owner == request.user
        else:
            return False


class IsUsersAddAPIUser(permissions.IsAdminUser):
    """
    Allows access only to special users created by admins to add users via /users/add API.
    """

    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'is_user_add_api_account') and request.user.is_user_add_api_account or super(IsUsersAddAPIUser, self).has_permission(request, view)
