from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, exceptions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, get_authorization_header


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    disable csrf check for authentication
    """

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class AllowAny(permissions.BasePermission):
    """
    Allow any access.
    This isn't strictly required, since you could use an empty
    permission_classes list, but it's useful because it makes the intention
    more explicit.
    """

    def has_permission(self, request, view):
        return True


class LoginAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.account.is_enabled)
