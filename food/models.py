from django.contrib.auth.models import User
from django.db import models


class Unit(models.Model):
    title = models.CharField(max_length=25)
    grams = models.FloatField()


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
    unit = models.ForeignKey(Unit)


class Dish(models.Model):
    OPTIONS = (
        'drink',
        'snack',
        'food'
    )
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=32, choices=[(e, e) for e in OPTIONS])
    description = models.TextField()
    preparation = models.TextField()
    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ingredient(models.Model):
    title = models.CharField(max_length=128)
    amount = models.FloatField(null=True, blank=True)
    unit = models.ForeignKey(Unit, null=True, blank=True)
    calories_per_unit = models.FloatField(default=0)
    nutrients_per_unit = models.ManyToManyField(Nutrient, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.FloatField(null=True, blank=True)
    units = models.ForeignKey(Unit, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Meal(models.Model):
    OPTIONS = (
        'Breakfast',
        'Lunch',
        'Dinner',
        'Supper',
        'Snack'
    )
    type = models.CharField(max_length=128, choices=[(e, e) for e in OPTIONS])
    dishes = models.ManyToManyField(Dish)


class DayPlan(models.Model):
    meals = models.ManyToManyField(Meal)


class Plan(models.Model):
    day_plans = models.ManyToManyField(DayPlan)
    description = models.TextField()
    goal = models.CharField(max_length=128)
    estimate_calories_per_day = models.PositiveIntegerField()
    estimate_protein_per_day = models.PositiveIntegerField()
    estimate_fat_per_day = models.PositiveIntegerField()
    estimate_carbohydrate_per_day = models.PositiveIntegerField()
