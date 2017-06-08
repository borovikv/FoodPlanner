from django.conf.urls import url
import food.views as f


urlpatterns = [
    url(r'^dishes$', f.dishes, name='dishes'),
    url(r'^dish/(?P<pk>\d+)$', f.dish, name='dish'),
]
