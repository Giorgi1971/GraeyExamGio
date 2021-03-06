from datetime import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices


class Ticket(models.Model):
    name = models.CharField(max_length=24, verbose_name='Name')
    start_time = models.DateTimeField(verbose_name='Start time', default=datetime(2021, 2, 3))
    end_time = models.DateTimeField(verbose_name="End time", default=datetime(2021, 2, 4))
    code = models.IntegerField(unique=True)
    price = models.IntegerField(default=12)

    class StatusType(TextChoices):
        FREE = 'Free', _("Free")
        SALED = 'Saled', _("Saled")

    status = models.CharField(max_length=5, choices=StatusType.choices, default=StatusType.FREE)

    def __str__(self):
        return f'{self.name} - {self.status}'

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')


class Order(models.Model):
    ticket = models.OneToOneField(
        to='Ticket', on_delete=models.CASCADE,
        related_name='orders'
    )
    t_price = models.IntegerField(default=0)
    sale_date = models.DateTimeField(verbose_name="Sale time", auto_now_add=True)
    user = models.ForeignKey(to='user.User', on_delete=models.PROTECT, related_name='orders')

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.t_price = self.ticket.price
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.ticket}-{self.t_price}-{self.sale_date}'
