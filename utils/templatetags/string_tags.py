import markdown
from django import template
from django.utils.safestring import mark_safe

import FoodPlanner.settings as settings
import food.utils as fu

register = template.Library()


@register.filter
def markdownify(content):
    return mark_safe(markdown.markdown(content, extensions=settings.MARKDOWNX_MARKDOWN_EXTENSIONS))


@register.filter
def dict_to_ingredients(json):
    return fu.dict_to_ingredients(json)
