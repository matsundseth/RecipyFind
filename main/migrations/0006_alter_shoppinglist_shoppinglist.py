# Generated by Django 4.0.2 on 2022-03-22 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_shoppinglist_shoppinglist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='shoppinglist',
            field=models.ManyToManyField(default='', to='main.Amount', verbose_name='shoppinglist'),
        ),
    ]
