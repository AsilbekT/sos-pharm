# Generated by Django 4.0.3 on 2022-03-30 17:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mobile', '0034_alter_sotuvchilar_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sotuvchilar',
            name='user',
        ),
        migrations.AddField(
            model_name='sotuvchilar',
            name='user',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
