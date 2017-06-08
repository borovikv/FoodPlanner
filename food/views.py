from django.shortcuts import render, get_object_or_404

import food.models as f


def dish(request, pk: str):
    obj = get_object_or_404(f.Dish, pk=pk)
    nutrients = sorted(obj.nutrients().items(), reverse=True)
    return render(request=request, template_name='dish.html', context=locals())


def dishes(request):
    all_dishes = f.Dish.objects.all()
    return render(request=request, template_name='dish.html', context={'dishes': all_dishes})