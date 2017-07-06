from django import template
from django import forms

register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})


@register.simple_tag
def add_attrs(field, **kwargs):
    attrs = field.field.widget.attrs
    attrs.update(kwargs)
    return field.as_widget(attrs=attrs)


@register.filter
def form_group(field: forms.Field):
    classes = ['form-group']
    if field.errors:
        classes.append('has-danger')
    return ' '.join(classes)
