from typing import List

from django import forms
from django.contrib.auth.models import User

import food.models as f
import tagging.models as t
import food.utils as u


class DishForm(forms.forms.Form):
    category = forms.ChoiceField(choices=[(e, e) for e in f.Dish.CATEGORY_OPTIONS])
    meals = forms.MultipleChoiceField(choices=[(e, e) for e in f.Meal.OPTIONS])
    ingredients = forms.CharField(widget=forms.Textarea())
    description = forms.CharField(widget=forms.Textarea())
    tags = forms.CharField(required=False)

    def save(self, user: 'User') -> 'f.Dish' or None:
        if self.is_valid():
            title, description = self.parse_description()
            dish = f.Dish(
                title=title,
                category=self.cleaned_data['category'],
                description=description,
                ingredients_json=self.get_ingredients_json(),
                owner=user,
            )
            dish.save()
            dish.tags = self.get_tags()
            dish.meals = self.get_meals()
            dish.save()
            return dish
        return None

    def get_tags(self) -> List['t.Tag']:
        tags = self.cleaned_data['tags'].split(' ')
        return list(t.Tag.objects.filter(title__in=tags).distinct())

    def parse_description(self) -> (str, str):
        description = self.cleaned_data['description']
        lines = description.strip().split('\n')
        return lines[0], '\n'.join(lines[1:]) if lines else ('', '')

    def get_meals(self):
        meals = self.cleaned_data['meals']
        print(meals)
        return list(f.Meal.objects.filter(title__in=meals))

    def get_ingredients_json(self) -> dict:
        ingredients = self.cleaned_data['ingredients']
        return u.get_ingredients(ingredients)
