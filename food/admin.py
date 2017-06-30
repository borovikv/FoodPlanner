from ajax_select.helpers import make_ajax_form
from django.contrib import admin
from django.db import models
from markdownx.admin import MarkdownxModelAdmin
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
class DishAdmin(MarkdownxModelAdmin):
    inlines = [
        DishIngredientAdmin
    ]

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }

    filter_horizontal = ('meals', )
    exclude = ('owner', )
    list_display = ('title', 'owner', 'meals_str')
    search_fields = ('title', 'description', )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.set_thumbnail()
        obj.set_ingredients_json()
        super(DishAdmin, self).save_model(request, obj, form, change)

    def meals_str(self, obj):
        return ', '.join(str(m) for m in obj.meals.all())


class IngredientNutrientAdmin(admin.TabularInline):
    model = food.IngredientNutrient
    extra = 0


class GrammsOfIngredientPerUnitInlineAdmin(admin.TabularInline):
    model = food.GramsOfIngredientPerUnit
    extra = 0


@admin.register(food.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [IngredientNutrientAdmin, GrammsOfIngredientPerUnitInlineAdmin]
    search_fields = ['title']