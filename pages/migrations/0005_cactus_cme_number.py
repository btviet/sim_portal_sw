# Generated by Django 4.0.10 on 2024-02-06 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_cactus_initial_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='cactus',
            name='cme_number',
            field=models.CharField(default='none', max_length=200),
        ),
    ]