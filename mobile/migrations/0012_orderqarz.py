# Generated by Django 4.0.3 on 2022-03-10 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0011_alter_aptekalar_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderQarz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('apteka', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mobile.aptekalar')),
                ('dorilar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mobile.dorilar')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mobile.order')),
            ],
        ),
    ]
