from django.conf.urls import url, include
import food.views as f


urlpatterns = [
    url(r'^dish/(?P<pk>\d+)$', f.dish),
]
