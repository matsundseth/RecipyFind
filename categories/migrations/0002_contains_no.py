# Generated by Django 4.0.2 on 2022-03-22 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contains',
            name='no',
            field=models.CharField(default='no', max_length=50),
        ),
    ]