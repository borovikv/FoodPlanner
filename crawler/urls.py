from django.conf.urls import url
import crawler.views as c

urlpatterns = [
    url(r'^$', c.Crawler.as_view(), name='crawler'),
]
