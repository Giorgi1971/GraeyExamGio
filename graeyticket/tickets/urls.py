from django.urls import path

from . import views
from .views import *

app_name = 'tickets'
urlpatterns = [
    path('', index, name='index'),
    path('tickets/', tickets, name='tickets'),
    path('personal/', personal, name='personal'),
    path('orders/', order, name='order'),
    # path('tickets/<int:pk>/', order_ticket, name='order_ticket'),
    path('tickets/<int:pk>/', order_ticket, name='order_ticket'),
    ]
