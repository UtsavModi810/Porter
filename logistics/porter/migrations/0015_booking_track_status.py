# Generated by Django 3.1.2 on 2021-03-24 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('porter', '0014_auto_20210324_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='track_status',
            field=models.PositiveIntegerField(default=0, max_length=2),
        ),
    ]
