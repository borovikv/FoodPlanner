from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from django.db import models

import datetime
from calendar import monthrange

import food.models as food


class Plan(models.Model):
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
        for i in monthrange(now.year, now.month):
            dishes = [self.get_dish(meal, i) for meal in self.meals()]
            # TODO: control ingredients and Plan goals
            self.days.create(order=i, dishes=dishes)

    def get_dish(self, meal: str, order: int) -> 'food.Dish':
        dishes = list(self.dishes.filter(meals__title=meal))
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




class PlanIngredient(models.Model):
    plan = models.ForeignKey(Plan, related_name='ingredients_goal')
    ingredient = models.ForeignKey(food.Ingredient)
    amount = models.PositiveIntegerField()
    unit = models.ForeignKey(food.Unit)

    def __str__(self):
        return '{plan} - {ingredient}'.format(plan=self.plan, ingredient=self.ingredient)


class DayPlan(models.Model):
    order = models.PositiveIntegerField()
    plan = models.ForeignKey(Plan, related_name='days')
    dishes = models.ManyToManyField(food.Dish)

    def __str__(self):
        return '{plan} #{order}'.format(plan=self.plan, order=self.order)

    class Meta:
        ordering = ['order']