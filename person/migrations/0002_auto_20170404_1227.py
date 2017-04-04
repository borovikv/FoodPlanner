# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 12:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_auto_20170404_1102'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DietPlanNutrient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('nutrient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.Nutrient')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nutrients_goal', to='person.DietPlan')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.Unit')),
            ],
        ),
        migrations.RemoveField(
            model_name='dietplaningredient',
            name='ingredient',
        ),
        migrations.RemoveField(
            model_name='dietplaningredient',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='dietplaningredient',
            name='unit',
        ),
        migrations.DeleteModel(
            name='DietPlanIngredient',
        ),
    ]
