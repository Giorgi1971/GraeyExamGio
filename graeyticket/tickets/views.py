from django.shortcuts import render
from decimal import Decimal
from typing import Dict, Optional
from django.core.paginator import Paginator
from django.shortcuts import render

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F, Sum, ExpressionWrapper, DecimalField, Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic

# from .forms import *
from .models import *
# Create your views here.


def index(request: WSGIRequest):
    ticket_list = Ticket.objects.all().order_by('-pk')
    context = {
        'form': ticket_list,
    }
    return render(request=request, template_name='tickets/index.html', context=context)
