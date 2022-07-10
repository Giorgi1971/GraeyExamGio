from django import forms
from .models import *


class DateTimeInput(forms.DateTimeInput):
    input_type = 'date'


class OrderModelForm1(forms.ModelForm):
    class Meta:
        widgets = {'sale_date': DateTimeInput()}
        model = Order
        fields = ('ticket',)
        # fields = '__all__'

    def __init__(self, *args, **kwargs): 
        super(OrderModelForm1, self).__init__(*args, **kwargs)
        self.fields['ticket'].queryset = Ticket.objects.filter(status = 'Free')
