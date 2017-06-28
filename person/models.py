import datetime
from calendar import monthrange

from django.contrib.auth.models import User
from django.db import models
from markdownx.models import MarkdownxField

import food.models as food


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


class DietPlan(models.Model):
    title = models.CharField(max_length=256)
    description = MarkdownxField(null=True, blank=True)
    user = models.ForeignKey(User)
    dishes = models.ManyToManyField(food.Dish)
    meals_per_day = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def today(self) -> 'DayPlan':
        total_days = self.days.count()
        if total_days:
            day = datetime.datetime.now().day
            return self.days.all()[day % total_days]

    def initialize(self):
        now = datetime.datetime.now()
        for day in monthrange(now.year, now.month):
            dishes = list(filter(lambda d: d, [self.get_dish(meal, day) for meal in self.meals()]))
            self.days.create(day=day, dishes=dishes)

