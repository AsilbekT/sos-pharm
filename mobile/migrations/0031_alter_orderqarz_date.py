# Generated by Django 4.0.3 on 2022-03-25 18:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0030_alter_orderqarz_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderqarz',
            name='date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]
