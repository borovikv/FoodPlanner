from ajax_select.helpers import make_ajax_form
from django.contrib import admin
from django.db import models
from markdownx.widgets import AdminMarkdownxWidget

import food.models as food


for m in (food.Unit, food.Nutrient, food.Meal):
    admin.site.register(m)


class DishIngredientAdmin(admin.TabularInline):
    model = food.DishIngredient
    form = make_ajax_form(food.DishIngredient, {
        'ingredient': 'ingredients'
    })
    extra = 1


@admin.register(food.Dish)
class DishAdmin(admin.ModelAdmin):
    inlines = [
        DishIngredientAdmin
    ]

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }

    filter_horizontal = ('meals', )


class IngredientNutrientAdmin(admin.TabularInline):
    model = food.IngredientNutrient
    extra = 0

class GrammsOfIngredientPerUnitInlineAdmin(admin.TabularInline):
    model = food.GrammsOfIngredientPerUnit
    extra = 0


@admin.register(food.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [IngredientNutrientAdmin, GrammsOfIngredientPerUnitInlineAdmin]
    search_fields = ['title']