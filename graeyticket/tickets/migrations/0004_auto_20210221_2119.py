# Generated by Django 3.1.7 on 2021-02-21 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_auto_20210221_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='t_price',
            field=models.IntegerField(default=0),
        ),
    ]
