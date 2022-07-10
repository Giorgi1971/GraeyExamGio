from django.conf import settings
from django.core.paginator import Paginator
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F, Sum, Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from requests import request
from .forms import *
from user.models import *
from .models import *
from django.views import generic
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib import messages


class IndexView(generic.ListView):
    template_name = 'tickets/tickets.html'
    context_object_name = 'ticket_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Ticket.objects.all().order_by('-pk')


def index(request: WSGIRequest):
    print(settings.BASE_DIR)
    if request.user.is_authenticated:
        return redirect('tickets:personal')
    return redirect('/tickets')


def return_ticket(request: WSGIRequest):
    order_form = OrderModelForm1()
    q1 = request.POST.get('return_ticket')
    if request.method == 'POST':
        # order_form = OrderModelForm1(request.POST)
        tick1 = Ticket.objects.all().get(pk=q1)
        if tick1.orders:
            user = tick1.orders.user
            print(tick1.__dict__)
            print(tick1.orders)
            print(tick1.orders.user)
            tick1.orders.delete()
            tick1.status = Ticket.StatusType.FREE
            user.salary += (tick1.price -1)
            tick1.save()
            user.save()
            return redirect('tickets:personal')
        else:
            return HttpResponse('Not Valid')
    else:
        return HttpResponse('Hello, Not Post')


def tickets(request: WSGIRequest):
    ticket_list = Ticket.objects.all().order_by('-pk')
    #  ბილეთების გასუფთავება, ეგრევე უნდა გავაკომენტარო, როგორც კი გასუფთავდება.
    # for i in ticket_list:
    #     i.status = 'Free'
    #     print (i)
    #     try:
    #         i.orders.delete()
    #         print (i.orders)
    #     except:
    #         continue
    #     i.save()
    context = {
        'ticket_list': ticket_list,
    }
    return render(request=request, template_name='tickets/tickets.html', context=context)


def personal(request: WSGIRequest) -> HttpResponse:
    order_form = OrderModelForm1()
    q1 = request.POST.get('ticket')
    if request.method == 'POST':
        order_form = OrderModelForm1(request.POST)
        if order_form.is_valid():
            tt = Ticket.objects.all().get(pk=q1)
            print(tt)
            user = request.user
            if user.salary >= tt.price:
                user.salary -= tt.price
            else:
                # Want to return message error !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! but not can
                messages.error(request, 'Not eneaf Money.')
                return redirect('tickets:personal') 
            order3 = order_form.save(commit=False)
            order3.user_id = request.user.id
            # order3.t_price = 1
            if q1:
                order3.ticket_id = request.POST['ticket']
            order3.save()

            user.save()
            tt.status = Ticket.StatusType.SALED
            tt.save()

    personal_page: User = get_object_or_404(User.objects.all(), pk=request.user.id)
    last: Order = personal_page.orders.all().order_by('-sale_date')
    if len(last) > 0:
        last = last[0]
    now = timezone.now()

    person_salary_info = personal_page.orders.all().annotate(
        earned_per_order=Sum('t_price')
        ).aggregate(
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
        ),
    )

    ticket_list = Ticket.objects.all().order_by('-pk')

    return render(request, template_name='tickets/personal.html', context={
        'form': order_form,
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
    order_list = Order.objects.filter(user=request.user.pk).filter(order_q).order_by('-pk')
    paginator = Paginator(order_list, 2)  # Show 12 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request=request, template_name='tickets/orders.html', context=context)
