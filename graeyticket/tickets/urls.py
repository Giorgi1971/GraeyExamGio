from django.urls import path
from django.contrib.auth.decorators import login_required as lr
from .views import *


app_name = 'tickets'

urlpatterns = [
    path('ind/', IndexView.as_view(), name='index'),
    path('', index, name='index'),
    path('tickets/', tickets, name='tickets'),
    path('return_ticket/', return_ticket, name='return_ticket'),
    path('personal/', lr(personal), name='personal'),
    path('orders/', lr(order), name='order'),
    ]
