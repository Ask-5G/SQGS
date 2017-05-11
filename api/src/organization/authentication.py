from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import check_password

from rest_framework import HTTP_HEADER_ENCODING, exceptions
from organization.models import Users


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_KEY', b'')
    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


def get_device_header(request):
    """
    Return request's 'Device:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    device = request.META.get('HTTP_DEVICE', b'')
    if isinstance(device, type('')):
        device = device.encode(HTTP_HEADER_ENCODING)
    return device


def validate_device_header(device):
    """
    Check for the valid  device header
    """
    if not device or device[0].lower() != b'type':
        msg = _('Invalid device header. No device type specificed.')
        raise exceptions.AuthenticationFailed(msg)
    if len(device) == 1:
        msg = _('Invalid device header. No device type specificed.')
        raise exceptions.AuthenticationFailed(msg)
    elif len(device) > 2:
        msg = _('Invalid device header.'
                'Device string should not contain spaces.')
        raise exceptions.AuthenticationFailed(msg)
    print device
    if device[1] == "mobile":
        return device
    else:
        msg = _('Invalid device header. '
                'Device type should either hub or mobile.')
        raise exceptions.AuthenticationFailed(msg)


def validate_auth_header(auth):
    if not auth or auth[0].lower() != b'token':
        msg = _('Invalid token header. No credentials provided.')
        raise exceptions.AuthenticationFailed(msg)
    if len(auth) == 1:
        msg = _('Invalid token header. No credentials provided.')
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = _('Invalid token header. '
                'Token string should not contain spaces.')
        raise exceptions.AuthenticationFailed(msg)
    return auth


def validate_token(token):
    if not token.is_active:
        raise exceptions.AuthenticationFailed(
            _('User inactive or deleted.'))
    elif token.is_expired:
        raise exceptions.AuthenticationFailed(
            _('Token has expired.'))
    return token


class BaseAuthentication(object):
    """
    All authentication classes should extend BaseAuthentication.
    """

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        raise NotImplementedError(".authenticate() must be overridden.")

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass


class SQGSTokenAuthentication(BaseAuthentication):
    """
    Based on the Device header the request
    authentication are from mobile or hub. For example:

        Device: Type mobile/hub

    Clients can authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    users_model = Users

    def authenticate(self, request):
        device = get_device_header(request).split()

        # Validate the device header
        device = validate_device_header(device)
        auth = get_authorization_header(request).split()

        # Validate the the auth header
        auth = validate_auth_header(auth)
        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _(
                'Invalid token header. '
                'Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_mobile(token)

    def authenticate_mobile(self, key):
        try:
            token = self.users_model.objects.get(key=key)
        except self.users_model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        token = validate_token(token)
        return (token, token)

    def authenticate_header(self, request):
        return 'Token'


class SQGSAuthentication(object):
    """
    Authenticate against Role and Password.
    """

    def authenticate_password(self, request):
        #import pdb;pdb.set_trace()
         if password:
             try:
                 user = Users.objects.get(name=name)
             except Users.DoesNotExist:
                 raise exceptions.AuthenticationFailed(_('Invalid user.'))
             if check_password(password, user.password):
                 return user
             else:
                 raise exceptions.AuthenticationFailed(
                     _('User password does not matches.'))
         return None

    def authenticate(self, request):
        return self.authenticate_password(request)
