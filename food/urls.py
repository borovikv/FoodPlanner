from django.conf.urls import url
import food.views as f


urlpatterns = [
    url(r'^dishes$', f.DishesView.as_view(), name='dishes'),
    url(r'^dish/(?P<pk>\d+)$', f.DishDetail.as_view(), name='dish'),
    url(r'^dish/$', f.DishSaver.as_view(), name='dish-saver'),
    url(r'^crawler/$', f.Crawler.as_view(), name='crawler'),
]
