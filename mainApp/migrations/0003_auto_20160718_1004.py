# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0002_films_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='films',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активность'),
        ),
    ]
