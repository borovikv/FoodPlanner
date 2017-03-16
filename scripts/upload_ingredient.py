import csv
import re

import food.models as food

path = '~/Downloads/пищевая ценность продуктов - Лист1.csv'

gr = food.Unit.objects.get_or_create(title='gramm', grams=1.0)


def get_title(key):
    return re.match(r'^([\w\s]+)\s+(г|мг)$', key)[1]


def get_unit(key):
    title = re.match(r'^([\w\s]+)\s+(г|мг)$', key)[2]
    if title == 'г':
        return gr
    if title == 'мг':
        return food.Unit.objects.get_or_create(title='mg', grams=0.001)


def main():
    with open(path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            ingredient = food.Ingredient()
            ingredient.title = row['Продукты']
            ingredient.amount = 100.0
            ingredient.unit = gr
            ingredient.calories_per_unit = row['Энерго-ценность, ккал']
            for key in row:
                if key in ['Энерго-ценность, ккал', 'Продукты']:
                    continue
                title = get_title(key)
                nutrient = food.Nutrient.filter(title=title).first()
                if not nutrient:
                    nutrient = food.Nutrient()
                    nutrient.title = title
                    nutrient.dri = 0
                    nutrient.unit = get_unit(key)
                    nutrient.save()
                ingredient.nutrients_per_unit.add(nutrient)
            ingredient.save()
