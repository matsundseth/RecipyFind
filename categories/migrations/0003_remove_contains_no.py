# Generated by Django 4.0.2 on 2022-03-22 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_contains_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contains',
            name='no',
        ),
    ]
