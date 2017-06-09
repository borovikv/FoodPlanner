import factory
import food.models as food


class UnitFactory(factory.Factory):
    class Meta:
        model = food.Unit

    title = food.Unit.GR


class NutrientFactory(factory.Factory):
    class Meta:
        model = food.Nutrient

    title = 'abracadabra',
    type = food.Nutrient.MACRO,
    dri = 1.1,
