from django.contrib import admin

import food.models as food

models = (
    food.Unit,
    food.Nutrient,
    food.Ingredient,
)
for m in models:
    admin.site.register(m)


class DishIngredientAdmin(admin.TabularInline):
    model = food.DishIngredient
    extra = 0


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