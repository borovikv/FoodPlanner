# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-12 07:23
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0012_auto_20170612_0634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='description_html',
        ),
        migrations.AlterField(
            model_name='dish',
            name='ingredients_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='nutrients_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]