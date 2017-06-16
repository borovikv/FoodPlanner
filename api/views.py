from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.renderers import JSONRenderer, AdminRenderer, BrowsableAPIRenderer
from rest_framework.response import Response

import food.models as food
from api.serializers import DishSerializer


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    renderer_classes = (JSONRenderer, AdminRenderer, BrowsableAPIRenderer)

    def get_queryset(self):
        if self.request.user.is_anonymous():
            return food.Dish.objects.none()
        return food.Dish.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @list_route()
    def recommendations(self, request):
        user = request.user
        print(user)
        queryset = food.Dish.objects.all()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page or queryset, many=True)

        if page:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

