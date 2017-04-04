import datetime
from collections import defaultdict
from calendar import monthrange
from typing import List

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from markdownx.models import MarkdownxField
from django.db import models

import food.models as food


class Info(models.Model):
    user = models.ForeignKey(User)
    age_years = models.PositiveIntegerField()
    height_cm = models.PositiveIntegerField()
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

    def get_dish(self, meal: str, order: int) -> 'food.Dish' or None:
        dishes = list(self.dishes.filter(meals__title=meal))
        if dishes:
            return dishes[order % len(dishes)]

    def meals(self):
        if self.meals_per_day == 1:
            return food.Meal.BREAKFAST,
        elif self.meals_per_day == 2:
            return food.Meal.BREAKFAST, food.Meal.SUPPER
        elif self.meals_per_day == 3:
            return food.Meal.BREAKFAST, food.Meal.DINNER, food.Meal.SUPPER
        elif self.meals_per_day > 3:
            return [food.Meal.BREAKFAST, food.Meal.DINNER, food.Meal.SUPPER] + [food.Meal.SNACK] * (self.meals_per_day - 3)

    def analyze(self, week=None):
        days = self.days.all()
        if week:
            day = week * 7
            days = days[day:day + 7]

        nutrients = self._collect_nutrients(days)
        result = {}
        for nutrient in nutrients:
            ingredient_plan = self.nutrients_goal.filter(nutrient=nutrient).first()
            if ingredient_plan:
                result[nutrient] = (nutrients[nutrient] / ingredient_plan.amount) * 100
            elif nutrient.dri:
                result[nutrient] = (nutrients[nutrient] / nutrient.dri) * 100
        return result

    # noinspection PyMethodMayBeStatic
    def _collect_nutrients(self, days: List['DayPlan']) -> dict:
        result = defaultdict(float)
        total_days = len(days)
        for day in days:
            for dish in day.dishes.all():
                dish_nutrients = dish.nutrients()
                for nutrient in dish_nutrients:
                    result[nutrient] += dish_nutrients[nutrient] / float(total_days)

        return result


class DietPlanNutrient(models.Model):
    plan = models.ForeignKey(DietPlan, related_name='nutrients_goal')
    nutrient = models.ForeignKey(food.Nutrient)
    amount = models.PositiveIntegerField()
    unit = models.ForeignKey(food.Unit)

    def __str__(self):
        return '{plan} - {ingredient}'.format(plan=self.plan, ingredient=self.ingredient)

    def clean(self):
        if not self.nutrient.is_correct_unit_for_nutrient_type(unit=self.unit):
            raise ValidationError(f'Incorrect unit {self.unit} for nutrient type {self.nutrient}:{self.nutrient.type}')


class DayPlan(models.Model):
    day = models.PositiveIntegerField()
    plan = models.ForeignKey(DietPlan, related_name='days')
    dishes = models.ManyToManyField(food.Dish)

    def __str__(self):
        return '{plan} #{order}'.format(plan=self.plan, order=self.day)

    class Meta:
        ordering = ['day']