from django.conf.urls import url
import food.views as f


urlpatterns = [
    url(r'^dishes$', f.DishesView.as_view(), name='dishes'),
    url(r'^dishes/(?P<pk>\d+)$', f.DishView.as_view(), name='dish'),
    url(r'^dishes/editing/(?P<pk>\d+)?$', f.DishCreate.as_view(), name='editing'),
]
