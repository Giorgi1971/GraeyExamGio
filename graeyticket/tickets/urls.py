from django.urls import path

from . import views
from .views import *

app_name = 'wellwash'
urlpatterns = [
    path('tickets', index, name='index'),
    ]
