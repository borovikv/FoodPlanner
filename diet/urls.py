from django.conf.urls import url
import diet.views as v

urlpatterns = [
    url(r'^$', v.DietsView.as_view(), name='diets'),
    url(r'^(?P<pk>[0-9]+)/$', v.DietDetail.as_view(), name='diet'),
]
