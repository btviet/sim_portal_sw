# Generated by Django 4.0.10 on 2024-02-06 09:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_remove_cactus_initial_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='cactus',
            name='initial_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 1, 0, 0), help_text='Time at 21.5 Rs'),
        ),
    ]