import requests
from bs4 import BeautifulSoup

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from crawler.forms import UrlForm, UrlsForm


class CsrfFreeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfFreeView, self).dispatch(request, *args, **kwargs)


# noinspection PyMethodMayBeStatic
class DishSaver(CsrfFreeView):
    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST or None)
        if form.is_valid():
            url = form.cleaned_data['url']
            response = requests.get(url)
            page = response.content
            soup = BeautifulSoup(page, "html.parser")

            result = soup.title
            return HttpResponse(result)

        return HttpResponseBadRequest()


# noinspection PyMethodMayBeStatic
class Crawler(View):
    def get(self, request, *args, **kwargs):
        form = UrlsForm()
        return render(request, 'form.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = UrlsForm(request.POST)
        if form.is_valid():
            return render(request, 'detail.html', context={'urls': form.urls()})


def create_dish(html):
    soup = BeautifulSoup(html, "html.parser")
