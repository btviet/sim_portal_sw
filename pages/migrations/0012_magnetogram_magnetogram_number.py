# Generated by Django 4.0.10 on 2024-02-07 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_remove_magnetogram_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='magnetogram',
            name='magnetogram_number',
            field=models.CharField(default='none', max_length=200),
        ),
    ]
