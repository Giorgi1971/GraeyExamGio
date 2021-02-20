from django import forms
from .models import *


class DateTimeInput(forms.DateTimeInput):
    input_type = 'date'


class OrderModelForm1(forms.ModelForm):
    class Meta:
        widgets = {'end_time': DateTimeInput(), 'start_time': DateTimeInput()}
        model = Order
        fields = ('ticket',)


class OrderModelForm2(forms.ModelForm):
    class Meta:
        widgets = {'end_time': DateTimeInput(), 'start_time': DateTimeInput()}
        model = Order
        fields = '__all__'
