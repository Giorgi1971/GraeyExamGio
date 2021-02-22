from django import forms
from .models import *


class DateTimeInput(forms.DateTimeInput):
    input_type = 'date'


class OrderModelForm1(forms.ModelForm):
    class Meta:
        widgets = {'sale_date': DateTimeInput()}
        model = Order
        fields = ('ticket',)
