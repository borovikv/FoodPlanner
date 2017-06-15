from rest_framework import serializers
import food.models as food


class DishSerializer(serializers.ModelSerializer):
    meals = serializers.SlugRelatedField(
        many=True,
        queryset=food.Meal.objects.all(),
        slug_field='title'
     )
    owner = serializers.StringRelatedField(many=False)

    class Meta:
        model = food.Dish
        exclude = ()
