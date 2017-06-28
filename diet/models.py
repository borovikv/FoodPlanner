from typing import Dict, List

from django.contrib.postgres.fields import JSONField
from django.db import models

import food.models as f


class Diet(models.Model):
    title = models.CharField(max_length=256)
    dishes = models.ManyToManyField(f.Dish, related_name='diets')
    meals = models.ManyToManyField(f.Meal, unique=True)
    number_of_weeks = models.IntegerField(default=4)
    # {day!int: mapOf(meal to dish)}
    days = JSONField(null=True, blank=True)

    def generate(self):
        self.number_of_weeks = self.days_to_dishes()

    def days_to_dishes(self) -> Dict[int, List[int]]:
        days_per_week = 7
        days = range(1, self.number_of_weeks * days_per_week + 1)
        return {day: self.get_dishes_for_day(day) for day in days}

    def get_dishes_for_day(self, day):
        return [self.get_dish(meal, day).pk for meal in self.meals]

    def get_dish(self, meal: str, day: int) -> 'f.Dish' or None:
        dishes = list(self.dishes.filter(meals__title=meal))
        if dishes:
            return dishes[day % len(dishes)]
