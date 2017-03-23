from django.shortcuts import render, get_object_or_404

import food.models as f


def dish(request, pk: str):
    obj = get_object_or_404(f.Dish, pk=pk)
    return render(request=request, template_name='dish.html', context=locals())
