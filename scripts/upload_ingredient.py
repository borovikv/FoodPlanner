import csv
import re

import food.models as food

path = '/Users/vborovic/Downloads/пищевая ценность продуктов - Лист1.csv'

gr = food.Unit.objects.get_or_create(title='gramm', grams=1.0)[0]


def get_title(key):
    return re.match(r'^([\w\s]+)\s+(г|мг)$', key)[1]


def get_unit(key):
    title = re.match(r'^([\w\s]+)\s+(г|мг)$', key)[2]
    if title == 'г':
        return gr
    if title == 'мг':
        return food.Unit.objects.get_or_create(title='mg', grams=0.001)[0]


def main():
    with open(path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            ingredient = food.Ingredient()
            ingredient.title = row['Продукты']
            ingredient.amount = 100.0
            ingredient.unit = gr
            ingredient.calories_per_unit = get_float(row, 'Энерго-ценность, ккал') or 17.0
            ingredient.save()
            for key in row:
                if key in ['Энерго-ценность, ккал', 'Продукты']:
                    continue
                title = get_title(key)
                nutrient = food.Nutrient.objects.filter(title=title).first()
                if not nutrient:
                    nutrient = food.Nutrient()
                    nutrient.title = title
                    nutrient.dri = 0
                    nutrient.dri_unit = get_unit(key)
                    nutrient.save()
                food.IngredientNutrient.objects.create(ingredient=ingredient, nutrient=nutrient, ammount=get_float(row, key), unit=get_unit(key))


def get_float(row, t):
    try:
        return float(row[t].replace(',', '.'))
    except:
        return None


main()