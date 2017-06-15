from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.authtoken import views

from api.views import DishViewSet


router = routers.DefaultRouter()
router.register(r'dishes', DishViewSet, 'dishes')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', views.obtain_auth_token),
]
