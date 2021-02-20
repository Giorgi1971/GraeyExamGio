# Generated by Django 3.1.7 on 2021-02-20 20:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_price', models.IntegerField()),
                ('sale_date', models.DateTimeField(auto_now_add=True, verbose_name='Sale time')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, verbose_name='Name')),
                ('start_time', models.DateTimeField(default=datetime.datetime(2021, 2, 3, 0, 0), verbose_name='Start time')),
                ('end_time', models.DateTimeField(default=datetime.datetime(2021, 2, 4, 0, 0), verbose_name='End time')),
                ('code', models.IntegerField(unique=True)),
                ('price', models.IntegerField(default=4)),
                ('status', models.CharField(choices=[('Free', 'Free'), ('Saled', 'Saled')], default='Free', max_length=5)),
            ],
        ),
    ]