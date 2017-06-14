from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import list_route
from rest_framework.renderers import JSONRenderer, AdminRenderer, BrowsableAPIRenderer
from rest_framework.response import Response

import food.models as food
from rest_api.serializers import DishSerializer


class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    renderer_classes = (JSONRenderer, AdminRenderer, BrowsableAPIRenderer)
    authentication_classes = (TokenAuthentication, BasicAuthentication)

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
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

