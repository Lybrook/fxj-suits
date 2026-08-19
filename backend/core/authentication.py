from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from .models import UserProfile


class UserProfileTokenAuthentication(BaseAuthentication):
    """Authenticate `Authorization: Token <user-token>` against UserProfile.auth_token."""

    keyword = b"token"

    def authenticate(self, request):
        header = get_authorization_header(request).split()
        if not header:
            return None
        if header[0].lower() != self.keyword:
            return None
        if len(header) != 2:
            raise AuthenticationFailed("Invalid token header. Use: Token <token>")

        token = header[1].decode("utf-8")
        user = UserProfile.objects.filter(auth_token=token).first()
        if not user:
            raise AuthenticationFailed("Invalid or expired token")
        return user, token

    def authenticate_header(self, request):
        return "Token"
