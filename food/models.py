import markdownx.models as markdown
from collections import defaultdict

from django.contrib.auth.models import User
from django.db import models


class Unit(models.Model):
    PREDEFINED_UNITS = {
        'gramm': 'gr',
        'milligramm': 'mg'
    }
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title

    def to_grams(self, ammount):
        if not ammount:
            return None
        if self.title == Unit.PREDEFINED_UNITS['gramm']:
            return ammount
        elif self.title == Unit.PREDEFINED_UNITS['milligramm']:
            return ammount / 1000.0

    def __lt__(self, other):
        """
        The more important units are created before less important thus they will have lower pk
        """
        return self.pk > other.pk

    def __gt__(self, other):
        """
        The more important units are created before less important thus they will have lower pk
        """
        return self.pk < other.pk

    def __eq__(self, other):
        if not other:
            return False
        return self.pk == other.pk


class Nutrient(models.Model):
    OPTIONS = (
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
    title = models.CharField(max_length=128, choices=[(e, e) for e in OPTIONS])
    dri = models.FloatField()
    dri_unit = models.ForeignKey(Unit)

    def __str__(self):
        return self.title

    def __gt__(self, other):
        return self.dri_unit > other.dri_unit or self.dri_unit == other.dri_unit and self.dri > other.dri

    def __lt__(self, other):
        return self.dri_unit < other.dri_unit or self.dri_unit == other.dri_unit and self.dri < other.dri

    def __eq__(self, other):
        if not other:
            return False
        return self.title == other.title


class Meal(models.Model):
    OPTIONS = (
        'Breakfast',
        'Lunch',
        'Dinner',
        'Supper',
        'Snack'
    )
    title = models.CharField(max_length=128, choices=[(e, e) for e in OPTIONS])

    def __str__(self):
        return self.title


class Dish(models.Model):
    OPTIONS = (
        'drink',
        'snack',
        'food'
    )
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=32, choices=[(e, e) for e in OPTIONS])
    meals = models.ManyToManyField(Meal)
    description = markdown.MarkdownxField()
    preparation = markdown.MarkdownxField()
    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def nutrients(self) -> list:
        nutrients_to_amount_per_unit = defaultdict(lambda: defaultdict(float))
        calories = 0
        for ingredient in self.ingredients.all():
            calories += ingredient.calories()
            for nutrient in ingredient.ingredient.nutrients.all():
                if nutrient.ammount:
                    nutrients_to_amount_per_unit[nutrient.nutrient][nutrient.unit] += ingredient.quantity() * nutrient.ammount

        result = []
        for n in dict(nutrients_to_amount_per_unit):
            amount_per_unit = nutrients_to_amount_per_unit[n]

            if len(amount_per_unit) == 1:
                result.append((n,) + tuple(amount_per_unit.items())[0])

        result.sort(key=lambda a: a[0])
        result.reverse()
        result = [('calories', 'kkal', calories)] + result
        return result


class Ingredient(models.Model):
    title = models.CharField(max_length=128)
    amount = models.FloatField(null=True, blank=True)
    calories_per_100_gr = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class IngredientNutrient(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='nutrients')
    nutrient = models.ForeignKey(Nutrient)
    ammount = models.FloatField(null=True, blank=True)
    unit = models.ForeignKey(Unit)

    def __str__(self):
        return str(self.nutrient)


class DishIngredient(models.Model):
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
        return self.convert_to_grams() / 100.0

    def convert_to_grams(self):
        c = GrammsOfIngredientPerUnit.objects.filter(ingredient=self.ingredient, unit=self.unit).first()
        return c.convert(self.amount)


class GrammsOfIngredientPerUnit(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='grams_per_unit_of_ingredient')
    unit = models.ForeignKey(Unit)
    grams = models.FloatField()

    def __str__(self):
        return '{unit} of {ingredient} = {grams}'.format(ingredient=self.ingredient, unit=self.unit_id, grams=self.grams)

    def convert(self, amount: float) -> float:
        """
        Convert amount of units to gramms
        :param amount: amount of units
        :return: grams
        """
        return self.grams * amount
