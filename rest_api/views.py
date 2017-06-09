from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer, AdminRenderer, BrowsableAPIRenderer

from rest_api.serializers import DishSerializer
import food.models as food


class DishViewSet(viewsets.ModelViewSet):
    queryset = food.Dish.objects.all()
    serializer_class = DishSerializer
    renderer_classes = (JSONRenderer, AdminRenderer, BrowsableAPIRenderer)
