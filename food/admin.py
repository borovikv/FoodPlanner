from ajax_select.helpers import make_ajax_form
from django.contrib import admin

import food.models as food

models = (
    food.Unit,
    food.Nutrient,
)
for m in models:
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


@admin.register(food.Meal)
class MealAdmin(admin.ModelAdmin):
    filter_horizontal = ['dishes']


@admin.register(food.DayPlan)
class DayPlanAdmin(admin.ModelAdmin):
    filter_horizontal = ['meals']


@admin.register(food.Plan)
class PlanAdmin(admin.ModelAdmin):
    filter_horizontal = ['day_plans']


class IngredientNutrientAdmin(admin.TabularInline):
    model = food.IngredientNutrient
    readonly_fields = list(filter(lambda n: n != 'id', map(lambda f: f.name, food.IngredientNutrient._meta.get_fields())))
    extra = 0


@admin.register(food.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [IngredientNutrientAdmin]