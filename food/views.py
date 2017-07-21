import io
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse
from django.views import generic as g
from django.views.generic.edit import FormView

import food.models as f
from food.forms import forms
from food.upload_ingredient import create_ingredients, MAPPING
from utils.forms import UploadFileForm


class DishesView(g.ListView):
    model = f.Dish
    template_name = 'dish/list.html'
    context_object_name = 'dishes'


class DishView(g.DetailView):
    model = f.Dish
    template_name = 'dish/detail.html'
    context_object_name = 'dish'

    def get_context_data(self, **kwargs):
        context = super(DishView, self).get_context_data(**kwargs)
        dish = context.get(self.context_object_name)
        context['nutrients'] = dish and sorted(dish.nutrients().items(), reverse=True) or []
        return context


class DishCreate(g.View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        dish = get_object_or_404(f.Dish, pk=pk) if pk else None
        form = forms.DishForm(instance=dish)
        return render(request, 'dish/form.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.DishForm(request.POST)
        if form.is_valid():
            dish = form.save(request.user)
            return HttpResponseRedirect(reverse('food:dish', kwargs=dict(pk=dish.pk)))
        return render(request, 'dish/form.html', context={'form': form})


class IngredientsView(FormView):
    form_class = UploadFileForm
    template_name = 'upload_file_form.html'
    success_url = '/admin'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            file = request.FILES['file']
            decoded_file = file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            create_ingredients(io_string, MAPPING)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
