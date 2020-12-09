from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path('register', register_user, name='register'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path(r'^confirm/(?P<token>[-a-zA-Z0-9_]+)/$', confirm_account, name='confirm'),
    path('unconfirmed/', account_confirmation, name='unconfirmed-account'),
]
