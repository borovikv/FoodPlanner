# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 08:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0009_auto_20170405_0810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='nutrient',
            name='dri_unit',
        ),
    ]
