import food.utils as subject


def test_get_ingredients():
    # GIVEN
    ingredients = '\n'.join((
        'яйца 4 шт',
        'сыр 50 г ',
        'ветчина 2 кусочка',
        'брокколи 100 г',
        'помидор 1',
        'болгарский перец 1',
        'соль',
        'перец',
    ))

    print(ingredients)
    # WHEN
    result = subject.get_ingredients(ingredients)

    # THEN
    print(result)
    assert result == {
        'яйца': {'unit': 'шт', 'order': 0, 'amount': '4'},
        'сыр': {'unit': 'г', 'order': 1, 'amount': '50'},
        'ветчина': {'unit': 'кусочка', 'order': 2, 'amount': '2'},
        'брокколи': {'unit': 'г', 'order': 3, 'amount': '100'},
        'помидор': {'unit': None, 'order': 4, 'amount': '1'},
        'болгарский перец': {'unit': None, 'order': 5, 'amount': '1'},
        'соль': {'unit': None, 'order': 6, 'amount': None},
        'перец': {'unit': None, 'order': 7, 'amount': None},
    }
