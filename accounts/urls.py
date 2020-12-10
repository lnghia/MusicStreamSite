from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path('register', register_user, name='register'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('confirm/<str:token>', confirm_account, name='confirm'),
    path('unconfirmed/', account_confirmation, name='unconfirmed-account'),
    path('resend_confirmation_email/', resend_confirmation_email, name='resend-confirmation-email'),
    path('link_expired/', confirmation_link_expired, name='confirmation-link-expired'),
]
