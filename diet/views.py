from django.views.generic import ListView, DetailView

from diet.models import Diet


class DietsView(ListView):
    model = Diet
    template_name = 'diet_list.html'


class DietDetail(DetailView):
    model = Diet
    template_name = 'diet_detail.html'
