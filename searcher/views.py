from django.views.generic import ListView

import food.models as f
from searcher.forms import SearchForm


class SearcherView(ListView):
    model = f.Dish
    template_name = 'dish/list.html'
    context_object_name = 'dishes'

    def get_queryset(self):
        form = SearchForm(self.request.GET or None)
        query = form.query_value
        if query:
            return super(SearcherView, self).get_queryset().filter(title__icontains=query)
        return super(SearcherView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(SearcherView, self).get_context_data(**kwargs)
        form = SearchForm(self.request.GET or None)
        context['query'] = form.query_value or ""
        return context
