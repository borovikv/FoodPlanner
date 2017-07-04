from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View

import requests
from bs4 import BeautifulSoup

import food.models as f
from food.forms import UrlForm, UrlsForm, SearchForm


class DishesView(ListView):
    model = f.Dish
    template_name = 'dishes.html'
    context_object_name = 'dishes'

    def get_queryset(self):
        form = SearchForm(self.request.GET or None)
        if form.is_valid():
            query = form.cleaned_data['query']
            return super(DishesView, self).get_queryset().filter(title__icontains=query)
        return super(DishesView, self).get_queryset()


class DishDetail(DetailView):
    model = f.Dish
    template_name = 'dish.html'
    context_object_name = 'dish'

    def get_context_data(self, **kwargs):
        context = super(DishDetail, self).get_context_data(**kwargs)
        dish = context.get(self.context_object_name)
        context['nutrients'] = dish and sorted(dish.nutrients().items(), reverse=True) or []
        return context


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
        print(form.fields)
        return render(request, 'crawler/form.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = UrlsForm(request.POST)
        if form.is_valid():
            return render(request, 'crawler/detail.html', context={'urls': form.urls()})


def create_dish(html):
    soup = BeautifulSoup(html, "html.parser")
