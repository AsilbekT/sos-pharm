# Generated by Django 4.0.3 on 2022-06-19 06:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0040_alter_orderqarz_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderqarz',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
