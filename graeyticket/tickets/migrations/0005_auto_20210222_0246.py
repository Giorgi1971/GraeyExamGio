# Generated by Django 3.1.7 on 2021-02-21 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20210221_2119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
    ]