# Generated by Django 3.1.2 on 2021-03-29 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('porter', '0018_booking_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprise',
            name='city_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='porter.city'),
            preserve_default=False,
        ),
    ]
