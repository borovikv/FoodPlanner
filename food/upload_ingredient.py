import csv
import re

from django.core.exceptions import ObjectDoesNotExist

import food.models as food

MAPPING = {
    'ingredient': {
        'title': 'Продукты',
    },
    'unit': {
        'to_internal': dict(
            zip(
                ['г', 'мг', 'ккал'],
                [food.Unit.GR, food.Unit.MG, food.Unit.KCAL]
            )
        )
    },
    'key_pattern': '([\w\s-]+,?)\s+(г|мг|ккал)'
}


def create_ingredients(csv_file: '_io.StringIO', mapping: dict):
    reader = csv.DictReader(csv_file)
    for row in reader:
        create_ingredient(row, mapping)


def create_ingredient(row, mapping):
    ingredient = get_or_create(food.Ingredient, title=row[mapping['ingredient']['title']])

    for key in row.keys():
        if key in mapping['ingredient'].values():
            continue

        nutrient = get_or_create_nutrient(key, mapping)

        food.IngredientNutrient.objects.create(
            ingredient=ingredient,
            nutrient=nutrient,
            amount_per_100_gr=get_float(row[key]),
            unit=get_unit(key, mapping)
        )


def get_or_create_nutrient(key, mapping):
    nutrient_title = get_title(key, mapping)
    nutrient_type = get_nutrient_type(key, mapping)
    return get_or_create(
        food.Nutrient,
        by_field='title',
        title=nutrient_title,
        type=nutrient_type,
        dri=0.0
    )


def get_title(key, mapping: dict):
    return re.match(mapping['key_pattern'], key)[1]


def unit_title_from_str(key, mapping):
    return re.match(mapping['key_pattern'], key)[2]


def get_nutrient_type(key: str, mapping: dict) -> str:
    title = unit_title_from_str(key, mapping)
    return dict((u, t) for t, u in food.Nutrient.TYPE_TO_UNIT.items())[mapping['unit']['to_internal'][title]]


def get_unit(key: str, mapping: dict) -> 'food.Unit':
    unit_title = unit_title_from_str(key, mapping)
    return get_or_create(food.Unit, title=mapping['unit']['to_internal'][unit_title])


def get_float(value):
    try:
        return float(value.replace(',', '.'))
    except:
        return None


def get_or_create(model, by_field=None, **kwargs):
    try:
        if by_field:
            obj = model.objects.get(**{by_field: kwargs[by_field]})
        else:
            obj = model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        obj = model(**kwargs)
        obj.save()
    return obj
