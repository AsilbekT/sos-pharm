# Generated by Django 4.0.3 on 2022-03-23 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0020_orderqarzitem_apteka_name_orderqarzitem_dori_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderqarzitem',
            name='day',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='orderqarzitem',
            name='month',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='orderqarzitem',
            name='year',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
