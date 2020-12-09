import re

from django.conf import settings
from django.contrib.auth import login
from django.http import response
from django.shortcuts import redirect

from .views import login_user

class IsActiveMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')

        if view_func.__name__ != login_user.__name__ and not request.user.is_anonymous:
            if not request.user.is_authenticated and not request.user.is_active:
                return redirect('accounts:unconfirmed-account')
        