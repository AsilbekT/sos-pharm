# Generated by Django 4.0.3 on 2022-03-23 19:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0023_alter_orderqarzitem_bought_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderqarzitem',
            name='bought_day',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
    ]