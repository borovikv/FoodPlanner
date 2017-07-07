from django import forms

import food.models as f
from food.forms.fields.IngredientsField import IngredientsField


class DishForm(forms.ModelForm):
    ingredients_json = IngredientsField()

    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)

    def save(self, user, commit=True) -> 'f.Dish':
        obj: f.Dish = super(DishForm, self).save(commit=False)

        obj.owner = user
        obj.title, obj.description = self.parse_description()
        if commit:
            obj.save()
            self.save_m2m()
        return obj

    def parse_description(self) -> (str, str):
        description = self.cleaned_data['description']
        lines = description.strip().split('\n')
        return lines[0], '\n'.join(lines[1:]) if lines else ('', '')

    class Meta:
        model = f.Dish
        fields = ('serving', 'ingredients_json', 'description', 'category', 'meals', 'tags')
