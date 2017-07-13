from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from crawler.forms import UrlForm, UrlsForm
from crawler.mapping import MAPPING


class CsrfFreeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CsrfFreeView, self).dispatch(request, *args, **kwargs)


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    page = response.content
    soup = BeautifulSoup(page, "html.parser")
    return soup


class DishSaver(CsrfFreeView):
    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST or None)
        if form.is_valid():
            url = form.cleaned_data['url']
            soup = get_soup(url)

            result = soup.title
            return HttpResponse(result)

        return HttpResponseBadRequest()


class Crawler(View):
    def get(self, request, *args, **kwargs):
        form = UrlsForm()
        return render(request, 'form.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = UrlsForm(request.POST)
        if form.is_valid():
            # titles = [parse_dish(url) for url in form.urls() if url.strip()]
            titles = set(urlparse(url).hostname for url in form.urls() if url.strip())
            return render(request, 'detail.html', context={'titles': titles})


def parse_dish(url):
    hostname = urlparse(url).hostname
    if not hostname:
        return
    soup = get_soup(url)
    mapper = MAPPING.get(hostname=hostname)
    return {m: soup.select(selector) for m, selector in mapper.items()}


def create_dish(html):
    soup = BeautifulSoup(html, "html.parser")
