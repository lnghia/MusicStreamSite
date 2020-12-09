import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RegistrationForm

# from ..utils.email.email_util import send_email
from utils.Email_Util import send_email

def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        data = {'email': email, 'password2': password2, 'password1': password1}
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.set_password(password1)
            form.save()
            confirmation_token = user.generate_confirmation_token()
            abs_url = request.build_absolute_uri(reverse('accounts:confirm', args=[confirmation_token]))
            send_email('Account Confirmation', email, {'url': abs_url}, 'mail/confirmation_email')
            return JsonResponse({"status": True, "message": "Registration confirm"})
        else:
            errors = []
            for field in form:
                for error in field.errors:
                    errors.append(error)
            return JsonResponse({"status": False, "errors": errors})
    else:
        return HttpResponse(json.dumps({"message": "Denied"}), content_type="application/json")


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        data = {'email': email, 'password': password}
        user = authenticate(username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": True, "message": "User logged in"})
        else:
            errors = ["User doesn't exists"]
            return JsonResponse({"status": False, "errors": errors})
    else:
        return HttpResponse(json.dumps({"message": "Denied"}), content_type="application/json")


def logout_user(request):
    logout(request)
    return redirect('core:home')

@login_required
def resend_confirmation_email(request):
    # hasattr(request, 'user')

    token = request.user.generate_confirmation_token()
    email = request.user.email

    send_email('Account Confirmation', email, {}, 'mail/confirmation_email')

    return redirect('unconfirmed-account')

@login_required
def account_confirmation(request):
    if not request.user.is_anonymous and not request.user.is_active:
        return render(request, 'account/unconfirmed.html', {'email': request.user.email})

    return redirect('core:home')

@login_required
def confirm_account(request, token):
    if not request.user.is_active:
        if request.user.verify_confirmation_token(token):
            request.user.is_active = True
            request.user.save()
    return redirect('core:home')
