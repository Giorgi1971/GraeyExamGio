from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from django.db.models import TextChoices


class Ticket(models.Model):
    name = models.CharField(max_length=24, verbose_name='Name')
    start_time = models.DateTimeField(verbose_name='Start time')
    end_time = models.DateTimeField(verbose_name="End time")
    code = models.IntegerField(unique=True)
    price = models.IntegerField(default=4)
    user = models.OneToOneField(to='user.User', on_delete=models.PROTECT, related_name='user_ticket')

    class StatusType(TextChoices):
        FREE = 'F', _("Free")
        SALED = 'S', _("Saled")

    status = models.CharField(max_length=1, choices=StatusType.choices, default=StatusType.FREE)


class Order(models.Model):
    ticket = models.ForeignKey(to='Ticket', on_delete=models.CASCADE, related_name='orders')
    t_price = models.IntegerField()
    sale_date = models.DateTimeField(verbose_name="Sale time", auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.t_price = self.ticket.price
        super(Order, self).save(*args, **kwargs)