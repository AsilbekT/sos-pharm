# Generated by Django 4.0.3 on 2022-09-16 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0042_alter_orderqarzitem_apteka_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderqarzitem',
            name='apteka_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
