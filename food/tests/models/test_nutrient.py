from django.test import TestCase
import food.models as food
import food.tests.factories as factories


class TestNutrient(TestCase):
    def test_is_correct_unit_for_nutrient_type_return_true_when_unit_match_type_macro(self):
        # GIVEN
        gr = factories.UnitFactory.create(title=food.Unit.GR)
        nutrient = factories.NutrientFactory.create(type=food.Nutrient.MACRO)

        # THEN
        self.assertTrue(nutrient.is_correct_unit_for_nutrient_type(gr))

    def test_is_correct_unit_for_nutrient_type_return_false_when_unit_do_not_match_type_macro(self):
        # GIVEN
        mg = factories.UnitFactory.create(title=food.Unit.MG)
        kcal = factories.UnitFactory.create(title=food.Unit.KCAL)
        nutrient = factories.NutrientFactory.create(type=food.Nutrient.MACRO)

        # THEN
        self.assertFalse(nutrient.is_correct_unit_for_nutrient_type(mg))
        self.assertFalse(nutrient.is_correct_unit_for_nutrient_type(kcal))

    def test_is_correct_unit_for_nutrient_type_return_true_when_unit_match_type_micro(self):
        # GIVEN
        mg = factories.UnitFactory.create(title=food.Unit.MG)
        nutrient = factories.NutrientFactory.create(type=food.Nutrient.MICRO)

        # THEN
        self.assertTrue(nutrient.is_correct_unit_for_nutrient_type(mg))

    def test_is_correct_unit_for_nutrient_type_return_false_when_unit_do_not_match_type_micro(self):
        # GIVEN
        gr = factories.UnitFactory.create(title=food.Unit.GR)
        kcal = factories.UnitFactory.create(title=food.Unit.KCAL)
        nutrient = factories.NutrientFactory.create(type=food.Nutrient.MICRO)

        # THEN
        self.assertFalse(nutrient.is_correct_unit_for_nutrient_type(gr))
        self.assertFalse(nutrient.is_correct_unit_for_nutrient_type(kcal))

    def test_is_correct_unit_for_nutrient_type_return_true_when_unit_match_type_energy(self):
        # GIVEN
        kcal = factories.UnitFactory.create(title=food.Unit.KCAL)
        nutrient = factories.NutrientFactory.create(type=food.Nutrient.ENERGY)

        # THEN
        self.assertTrue(nutrient.is_correct_unit_for_nutrient_type(kcal))

    def test_is_correct_unit_for_nutrient_type_return_false_when_unit_do_not_match_type_energy(self):
        # GIVEN
        mg = factories.UnitFactory.create(title=food.Unit.MG)
        gr = factories.UnitFactory.create(title=food.Unit.GR)
        nutrient = factories.NutrientFactory.create(type=food.Nutrient.ENERGY)

        # THEN
        self.assertFalse(nutrient.is_correct_unit_for_nutrient_type(gr))
        self.assertFalse(nutrient.is_correct_unit_for_nutrient_type(mg))
