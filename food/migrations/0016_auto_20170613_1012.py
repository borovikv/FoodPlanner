# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-13 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0015_auto_20170613_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientnutrient',
            name='amount_per_100_gr',
            field=models.FloatField(default=0),
        ),
    ]