from django.conf.urls import url, include

from rest_framework import routers

from rest_api.views import DishViewSet


router = routers.DefaultRouter()
router.register(r'dishes', DishViewSet, 'dishes')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
]
