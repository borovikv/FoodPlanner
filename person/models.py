from django.contrib.auth.models import User
from django.db import models


class Info(models.Model):
    user = models.ForeignKey(User)
    age_years = models.PositiveIntegerField()
    height_cm = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Weight(models.Model):
    user = models.ForeignKey(User)
    weight_kg = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
