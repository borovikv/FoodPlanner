import random
from typing import List

from collections import defaultdict
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from markdownx.models import MarkdownxField

import food.models as f
from diet.utils import meals, convert_to_grams


class Diet(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=256)
    description = MarkdownxField(null=True, blank=True)
    dishes = models.ManyToManyField(f.Dish, related_name='diets')
    number_of_meals = models.IntegerField(default=4)
    number_of_weeks = models.IntegerField(null=True, blank=True)
    number_of_days = models.IntegerField(null=True, blank=True)
    # {day!int: mapOf(meal to dish)}
    days = JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.number_of_weeks and not self.number_of_days:
            raise ValidationError('You have to set either number of weeks or number of days')
        elif self.number_of_weeks and self.number_of_days:
            raise ValidationError('You have to set only number of weeks or number of days')

    def generate(self):
        self.days = self.days_to_dishes()

    def days_to_dishes(self) -> List[List[int]]:
        dishes = [self.get_dishes_for_meal(meal) for meal in meals(self.number_of_meals)]

        return [self.one_day_dishes(dishes) for _ in self.total_days]

    @property
    def total_days(self):
        total_days = self.number_of_days if self.number_of_days else self.number_of_weeks * 7
        return range(1, total_days + 1)

    @staticmethod
    def one_day_dishes(dishes: List[List['f.Dish']]) -> List[int]:
        result = []
        for meal_dishes in dishes:
            random.shuffle(meal_dishes)
            for dish in meal_dishes:
                if dish.pk not in result:
                    result.append(dish.pk)
                    break

        if len(result) < len(dishes):
            candidates = [d.pk for meal_dishes in dishes for d in meal_dishes if d.pk not in result]
            if not candidates:
                candidates = list(result)
            random.shuffle(candidates)

            result += [candidates[i % len(candidates)] for i in range(len(dishes) - len(result))]

        return result

    def get_dishes_for_meal(self, meal):
        return list(self.dishes.filter(meals__title=meal).distinct())

    def day_dishes(self, from_day=0, to_day=None):
        if not to_day:
            to_day = len(self.days)

        if from_day > to_day:
            return []
        return [[self.dishes.filter(pk=pk).first() for pk in day] for day in self.days[from_day: to_day]]

    def ingredients_for_period(self, from_day=0, to_day=None):
        dishes = sum(self.day_dishes(from_day=from_day, to_day=to_day), [])
        ingredients = defaultdict(list)
        for dish in dishes:
            ingredient_to_amount = dish.ingredient_to_amount()
            for ingredient, amount in ingredient_to_amount.items():
                ingredients[ingredient].append(amount)

        result = {}
        for ingredient, amounts in ingredients.items():
            total_g = sum(convert_to_grams(ingredient, amount['amount'], amount['unit']) for amount in amounts)
            result[ingredient] = total_g, f.Unit.GR

        return result

    def counted_dishes(self, from_day=0, to_day=None):
        dishes = sum(self.day_dishes(from_day=from_day, to_day=to_day), [])
        result = defaultdict(int)
        for d in dishes:
            result[d] += 1
        return result.items()
