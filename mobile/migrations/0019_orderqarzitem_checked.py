# Generated by Django 4.0.3 on 2022-03-21 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0018_orderqarzitem_qoldi_orderqarzitem_umumiy_summa'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderqarzitem',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]