from django.urls import path
from django.contrib.auth.decorators import login_required as lr


from . import views
from .views import *

app_name = 'tickets'
urlpatterns = [
    path('', index, name='index'),
    path('tickets/', tickets, name='tickets'),
    path('personal/', lr(personal), name='personal'),
    path('orders/', lr(order), name='order'),
    ]
