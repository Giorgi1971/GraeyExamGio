from django.conf import settings
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from .forms import *


def user_registration(request):
    user_create_form = CustomUserCreationForm()
    print('1')
    if request.method == 'POST':
        user_create_form: CustomUserCreationForm = CustomUserCreationForm(request.POST)
        print('2')
        if user_create_form.is_valid():
            print('3')
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
