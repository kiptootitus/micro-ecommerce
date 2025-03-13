# myapp/middleware.py

import threading

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

_local = threading.local()


class CurrentUserMiddleware:
    def process_request(self, request):
        auth = JWTAuthentication()
        try:
            user, _ = auth.authenticate(request)

            request.user = user  # Set authenticated user manually
        except AuthenticationFailed:
            request.user = None  # Keep as AnonymousUser if token is invalid

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _local.user = request.user

        response = self.get_response(request)
        return response


def get_current_user():
    return getattr(_local, 'user', None)