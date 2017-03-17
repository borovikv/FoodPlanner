from ajax_select import register, LookupChannel
from .models import Ingredient


@register('ingredients')
class IngredientLookup(LookupChannel):

    model = Ingredient

    def get_query(self, q, request):
        return self.model.objects.filter(title__icontains=q).order_by('title')[:50]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.title