from django import forms
import food.utils as u


class IngredientsField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.widget = forms.Textarea()
        super(IngredientsField, self).__init__(*args, **kwargs)

    def has_changed(self, initial, data):
        return self.prepare_value(initial) != data

    def to_python(self, value) -> dict:
        if not value:
            return {}
        return u.ingredients_to_dict(value)

    def prepare_value(self, value: dict) -> str:
        try:
            return '\n'.join(u.dict_to_ingredients(value))
        except AttributeError:
            return str(value if value is not None else '')
