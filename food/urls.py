from django.conf.urls import url
import food.views as f


urlpatterns = [
    url(r'^dishes$', f.DishesView.as_view(), name='dishes'),
    url(r'^dish/(?P<pk>\d+)$', f.DishView.as_view(), name='dish'),
    url(r'^dish/create$', f.DishCreate.as_view(), name='create'),
]
