import re
from collections import defaultdict
from typing import Dict

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
import markdownx.models as markdown

import tagging.models as t


class Unit(models.Model):
    GR = 'g'
    MG = 'mg'
    KCAL = 'kcal'
    PREDEFINED_UNITS = {
        'gram': GR,
        'milligram': MG,
        KCAL: KCAL,
    }
    title = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.title

    def to_grams(self, ammount):
        if not ammount:
            return None
        if self.title == Unit.PREDEFINED_UNITS['gramm']:
            return ammount
        elif self.title == Unit.PREDEFINED_UNITS['milligramm']:
            return ammount / 1000.0


class Nutrient(models.Model):
    OPTIONS = (
        'KCal',
        'Total Fat',
        'Saturated FatMonounsaturated Fat',
        'Polyunsaturated Fat',
        'Total trans fatty acids',
        'Total trans-monoenoic fatty acids',
        'Total trans-polyenoic fatty acids',
        'Total Omega-3 fatty acids',
        'Total Omega-6 fatty acids',
        'Total carbohydrate',
        'Added sugars',
        'Dietary fiber',
        'Vitamin A',
        'Vitamin C',
        'Vitamin D',
        'Vitamin E',
        'Vitamin K',
        'Thiamin (vitamin B1)',
        'Riboflavin (vitamin B2)',
        'Niacin (vitamin B3)',
        'Pyridoxine (vitamin B6)',
        'Folate',
        'Cobalamine (vitamin B12)',
        'Biotin',
        'Pantothenic acid (vitamin B5)',
        'Calcium',
        'Iron',
        'Phosphorus',
        'Iodine',
        'Magnesium',
        'Zinc',
        'Selenium',
        'Copper',
        'Manganese',
        'Protein'
    )
    MACRO = 'macro'
    MICRO = 'micro'
    ENERGY = 'energy'
    TYPE_ORDER = [ENERGY, MACRO, MICRO]
    TYPE_TO_UNIT = {MACRO: Unit.GR, MICRO: Unit.MG, ENERGY: Unit.KCAL}

    title = models.CharField(max_length=128, choices=[(e, e) for e in OPTIONS], unique=True)
    type = models.CharField(max_length=10, choices=((MACRO, MACRO), (MICRO, MICRO), (ENERGY, ENERGY),))
    dri = models.FloatField()

    def __str__(self):
        return self.title

    def __gt__(self, other: 'Nutrient'):
        return self._position() > other._position() or self.type == other.type and self.dri > other.dri

    def _position(self):
        return 1.0 / self.TYPE_ORDER.index(self.type)

    def __lt__(self, other: 'Nutrient'):
        return self._position() < other._position() or self.type == other.type and self.dri < other.dri

    def __eq__(self, other):
        if not other:
            return False
        return self.title == other.title

    def is_correct_unit_for_nutrient_type(self, unit):
        return self.default_unit_title() == unit.title

    def default_unit_title(self):
        return self.TYPE_TO_UNIT[self.type]


class Meal(models.Model):
    BREAKFAST = 'BREAKFAST'
    LUNCH = 'LUNCH'
    DINNER = 'DINNER'
    SUPPER = 'SUPPER'
    SNACK = 'SNACK'
    OPTIONS = (
        BREAKFAST,
        LUNCH,
        DINNER,
        SUPPER,
        SNACK,
    )
    title = models.CharField(max_length=128, choices=[(e, e) for e in OPTIONS], unique=True)

    def __str__(self):
        return self.title


class Dish(models.Model):
    CATEGORY_OPTIONS = (
        'drink',
        'snack',
        'food'
    )
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=32, choices=[(e, e) for e in CATEGORY_OPTIONS])
    meals = models.ManyToManyField(Meal)
    serving = models.PositiveIntegerField()
    description = markdown.MarkdownxField()
    thumbnail = models.ImageField(null=True, blank=True)
    ingredients_json = JSONField(null=True, blank=True)
    nutrients_json = JSONField(null=True, blank=True)
    owner = models.ForeignKey(User)
    tags = models.ManyToManyField(t.Tag, related_name='dishes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def nutrients(self) -> Dict[Nutrient, float]:
        """
        :return: amount of nutrients per dish
        """
        nutrients_to_amount_per_unit = defaultdict(float)
        for dish_ingredient in self.ingredients.all():
            ingredient_quantity = dish_ingredient.quantity()
            for nutrient in dish_ingredient.ingredient.nutrients.all():
                if not nutrient.amount_per_100_gr:
                    continue

                nutrients_to_amount_per_unit[nutrient.nutrient] += ingredient_quantity * nutrient.amount_per_100_gr

        return dict(nutrients_to_amount_per_unit)

    @classmethod
    def nutrients_from_json(cls, ingredients_json) -> Dict[str, float]:
        """
        :return: amount of nutrients per dish
        """
        nutrients_to_amount_per_unit = defaultdict(float)
        for title, amount in ingredients_json.items():
            ingredient = Ingredient.objects.filter(title__iexact=title).first()
            if not ingredient:
                continue
            ingredient_quantity = quantity(ingredient=title, amount=amount['amount'], unit=amount['unit'])
            for nutrient in ingredient.nutrients.all():
                nutrients_to_amount_per_unit[nutrient.nutrient] += ingredient_quantity * nutrient.amount_per_100_gr

        return dict(nutrients_to_amount_per_unit)

    def set_thumbnail(self):
        path_match = re.match(r'!\[\]\(/media/(?P<path>markdownx/[0-9a-z-]+.jpg)\)', self.description)
        if path_match:
            self.thumbnail = path_match.group('path')

    def set_nutrients_json(self):
        nutrients = self.nutrients() or self.nutrients_from_json(self.ingredients_json)
        self.nutrients_json = {str(nutrient): amount for nutrient, amount in nutrients.items()}

    def set_ingredients_json(self):
        self.ingredients_json = {
            str(ingredient.ingredient): {
                'amount': ingredient.amount,
                'unit': str(ingredient.unit),
                'order': i
            }
            for i, ingredient in enumerate(self.ingredients.all())
        }

    def ingredient_to_amount(self):
        return self.ingredients_json

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.set_nutrients_json()
        super(Dish, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class Ingredient(models.Model):
    title = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class IngredientNutrient(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='nutrients')
    nutrient = models.ForeignKey(Nutrient)
    amount_per_100_gr = models.FloatField(default=0, null=True, blank=True)
    unit = models.ForeignKey(Unit)

    def __str__(self):
        return str(self.nutrient)

    def clean(self):
        if not self.nutrient.is_correct_unit_for_nutrient_type(unit=self.unit):
            raise ValidationError(f'Incorrect unit {self.unit} for nutrient type {self.nutrient}:{self.nutrient.type}')


class DishIngredient(models.Model):
    # todo: remove this class
    """
    This class is used only for django admin fill ingredients
    It should be removed as soon as custom admin form for json fields will be created
    """
    dish = models.ForeignKey(Dish, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, related_name='dishes')
    amount = models.FloatField(null=True, blank=True)
    unit = models.ForeignKey(Unit, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ingredient)

    def calories(self) -> float:
        return self.quantity() * self.ingredient.calories_per_100_gr

    def quantity(self) -> float:
        """
        how many 100 gr units included in total grams of this ingredient in dish
        for example:
        shake: 20 gr protein powder, 100 gr milk
        quantity for protein powder will be 20 / 100 = 0.2
                     milk           will be 100 / 100 = 1
        :return: coefficient of how many 100 gr units included in total grams of this ingredient in dish
        """
        return quantity(ingredient=self.ingredient.title, amount=self.amount, unit=self.unit.title)


class GramsOfIngredientPerUnit(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='grams_per_unit_of_ingredient')
    unit = models.ForeignKey(Unit)
    grams = models.FloatField()

    def __str__(self):
        return '{unit} of {ingredient} = {grams}'.format(ingredient=self.ingredient, unit=self.unit_id,
                                                         grams=self.grams)

    def convert(self, amount: float) -> float:
        """
        Convert amount of units to gramms
        :param amount: amount of units
        :return: grams
        """
        return self.grams * amount

    @classmethod
    def convert_to_grams(cls, ingredient: str, unit: str, amount) -> float:
        try:
            return cls.objects.get(
                ingredient__title__iexact=ingredient,
                unit__title__iexact=unit
            ).convert(amount)
        except:
            return 0


def quantity(ingredient: str, unit: str, amount: float):
    """
    how many 100 gr units included in total grams of this ingredient in dish
    for example:
    shake: 20 gr protein powder, 100 gr milk
    quantity for protein powder will be 20 / 100 = 0.2
                 milk           will be 100 / 100 = 1
    :return: coefficient of how many 100 gr units included in total grams of this ingredient in dish
    """
    return GramsOfIngredientPerUnit.convert_to_grams(ingredient=ingredient, amount=float(amount), unit=unit) / 100.0
