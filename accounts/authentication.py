from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from .models import AuthToken


class AnonymousUser:
    """Minimal stand-in for django.contrib.auth's AnonymousUser, which can't
    be imported because the auth/contenttypes apps are not installed."""

    pk = None
    id = None
    phone_hash = ''
    display_name = ''
    is_active = False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def __str__(self):
        return 'AnonymousUser'


class AppTokenAuthentication(BaseAuthentication):
    """Token auth backed by our own auth_tokens table.

    Clients send:  Authorization: Token <key>
    """

    keyword = 'Token'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        if len(auth) != 2:
            raise exceptions.AuthenticationFailed('Invalid token header.')

        try:
            key = auth[1].decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed('Invalid token header.')

        try:
            token = AuthToken.objects.select_related('user').get(key=key)
        except AuthToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword
