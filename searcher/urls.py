from django.conf.urls import url
import searcher.views as s

urlpatterns = [
    url(r'^$', s.SearcherView.as_view(), name='search'),
]
