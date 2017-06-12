from rest_framework import serializers
import food.models as food


class DishSerializer(serializers.ModelSerializer):
    meals = serializers.StringRelatedField(many=True)
    owner = serializers.StringRelatedField(many=False)

    class Meta:
        model = food.Dish
        exclude = ()
