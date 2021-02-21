from django.shortcuts import render
from decimal import Decimal
from typing import Dict, Optional
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db import models

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F, Sum, ExpressionWrapper, DecimalField, Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic

from .forms import *
from user.models import *
from .models import *
# Create your views here.


def index(request: WSGIRequest):
    if request.user.is_authenticated:
        return redirect('tickets:personal')
    return redirect('/tickets')


def tickets(request: WSGIRequest):
    ticket_list = Ticket.objects.all()
    context = {
        'ticket_list': ticket_list,
    }
    return render(request=request, template_name='tickets/tickets.html', context=context)


def order_ticket(request: WSGIRequest, pk: int) -> HttpResponse:
    order_form = OrderModelForm1()
    q1 = request.POST.get('q')
    if request.method == 'POST' and q1:
        order_form = OrderModelForm1(request.POST)
        print(q1)

    order_q = Q()
    if q1:
        order_q &= Q(ticket__name__icontains=q1)

        if order_form.is_valid():
            order1 = order_form.save(commit=False)
            order1
            order1.save()
            return redirect('../')

    return render(request, template_name='tickets/personal.html', context={
        'form': order_form
    })


def personal(request: WSGIRequest) -> HttpResponse:
    order_form1 = OrderModelForm1()
    order_form2 = OrderModelForm2()
    q1 = request.POST.get('q')
    if q1 and request.method == 'POST':
        order_form2 = OrderModelForm2(request.POST)
        print(q1)
        if order_form2.is_valid():
            order1 = order_form2.save(commit=False)
            order1.save()
        else:
            print('+-+-+-')

    if not q1 and request.method == 'POST':

        order_form1 = OrderModelForm1(request.POST)
        if order_form1.is_valid():
            order1 = order_form1.save(commit=False)
            order1.user_id = request.user.id
            order1.t_price = 1
            order1.save()
            tt = Ticket.objects.all().get(pk=order1.ticket_id)
            tt.status = Ticket.StatusType.SALED
            tt.save()

    personal_page: User = get_object_or_404(User.objects.all(), pk=request.user.id)
    print(personal_page)
    last = personal_page.orders.all().order_by('-sale_date')[0]
    print(last)
    now = timezone.now()

    person_salary_info = personal_page.orders.all().annotate(
        earned_per_order=Sum('t_price')).aggregate(
        earned_money_year=Sum(
            'earned_per_order',
            filter=Q(sale_date__gte=now - timezone.timedelta(days=365))
        ),
        washed_last_year=Count(
            'id',
            filter=Q(sale_date__gte=now - timezone.timedelta(days=365))
        ),
        earned_money_month=Sum(
            'earned_per_order',
            filter=Q(sale_date__gte=now - timezone.timedelta(weeks=4))
        ),
        washed_last_month=Count(
            'id',
            filter=Q(sale_date__gte=now - timezone.timedelta(weeks=4))
        ),
        earned_money_week=Sum(
            'earned_per_order',
            filter=Q(sale_date__gte=now - timezone.timedelta(days=7))
        ),
        washed_last_week=Count(
            'id',
            filter=Q(sale_date__gte=now - timezone.timedelta(days=7))
        )
    )

    ticket_list = Ticket.objects.all().order_by('-pk')

    return render(request, template_name='tickets/personal.html', context={
        'form': order_form1,
        'personal': personal_page,
        'ticket_list': ticket_list,
        'last': last,
        **person_salary_info,
    })


def order(request: WSGIRequest):
    order_q = Q()
    q1 = request.GET.get('name')
    if q1:
        order_q &= Q(ticket__name__icontains=q1)
    order_list = Order.objects.filter(order_q).order_by('-pk')
    paginator = Paginator(order_list, 4)  # Show 12 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request=request, template_name='tickets/orders.html', context=context)
