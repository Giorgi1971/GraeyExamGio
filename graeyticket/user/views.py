from django.conf import settings
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import *
from django.core.mail import send_mail


def user_registration(request):
    user_create_form = CustomUserCreationForm()
    if request.method == 'POST':
        user_create_form: CustomUserCreationForm = CustomUserCreationForm(request.POST, files=request.FILES)
        if user_create_form.is_valid():
            customer: User = user_create_form.save(commit=False)
            customer.save()
            return redirect('user:user_login')

    return render(
        request,
        template_name='user/registration.html',
        context={
            'form': user_create_form
        }
    )


def user_login(request):
    if request.user.is_authenticated:
        return redirect('tickets:index')
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('tickets:index')

    return render(
        request,
        'user/login.html',
        context={
            'form': form
        }
    )


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
    return HttpResponse(status=405)
