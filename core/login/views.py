from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from core.forms import LoginForm, SignUpForm, ResetPasswordForm
from core.models import CustomUser
import uuid
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, 'Invalid credentials.')
    return render(request, "core/login/login.html", {"form": form})

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User created successfully.')
            return redirect("/login")
        else:
            messages.error(request, 'Form is not valid.')
    else:
        form = SignUpForm()
    return render(request, "core/login/register.html", {"form": form})


def reset_password(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            try:
                user = CustomUser.objects.get(email=email)
                token = str(uuid.uuid4())
                user.reset_password_token = token
                user.reset_password_expire = timezone.now() + timedelta(hours=24)
                user.save()

                reset_link = f"{request.scheme}://{request.get_host()}/reset-password-confirm/{token}"
                send_mail(
                    'Password Reset Request',
                    f'Click this link to reset your password: {reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Password reset link has been sent to your email.')
                return redirect("/login")
            except CustomUser.DoesNotExist:
                messages.error(request, 'No user found with this email address.')
    else:
        form = ResetPasswordForm()
    return render(request, "core/login/reset_password.html", {"form": form})