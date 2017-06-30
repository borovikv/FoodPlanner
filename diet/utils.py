import food.models as food
from typing import Tuple


def meals(amount: int) -> Tuple[str]:
    m = [(food.Meal.BREAKFAST,),
         (food.Meal.BREAKFAST, food.Meal.SUPPER),
         (food.Meal.BREAKFAST, food.Meal.DINNER, food.Meal.SUPPER),
         (food.Meal.BREAKFAST, food.Meal.DINNER, food.Meal.SUPPER) + (food.Meal.SNACK,) * (amount - 3)]
    return m[amount - 1 if amount <= len(m) else -1]
