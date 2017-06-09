from rest_framework import serializers
import food.models as food


class DishSerializer(serializers.ModelSerializer):
    meals = serializers.StringRelatedField(many=True)
    nutrients = serializers.SerializerMethodField()
    owner = serializers.StringRelatedField(many=False)

    # noinspection PyMethodMayBeStatic
    def get_nutrients(self, obj: food.Dish):
        return {str(key): value for key, value in obj.nutrients().items()}

    class Meta:
        model = food.Dish
        exclude = ('description', 'preparation')
