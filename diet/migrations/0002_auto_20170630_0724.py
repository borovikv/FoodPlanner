# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-30 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diet',
            name='number_of_days',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='diet',
            name='number_of_weeks',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
