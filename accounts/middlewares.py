import re

from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render
from django.urls import resolve

from .views import *

class IsActiveMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')

        app_name = resolve(request.path).app_name

        print(app_name)

        allowed_apps = {
            'accounts'
        }

        if not request.user.is_anonymous and app_name not in allowed_apps:
            if request.user.is_authenticated and not request.user.is_active:
                return render(request, 'account/unconfirmed.html', {'email': request.user.email})
        