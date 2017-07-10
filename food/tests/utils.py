import food.utils as subject


def test_get_ingredients_when_amounts_from_end():
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

    # WHEN
    result = subject.ingredients_to_dict(ingredients)

    # THEN
    print(result)
    assert result == {
        'яйца': {'order': 0, 'amount': [('4', 'шт')]},
        'сыр': {'order': 1, 'amount': [('50', 'г')]},
        'ветчина': {'order': 2, 'amount': [('2', 'кусоч')]},
        'брокколи': {'order': 3, 'amount': [('100', 'г')]},
        'помидор': {'order': 4, 'amount': [('1', '')]},
        'болгарский перец': {'order': 5, 'amount': [('1', '')]},
        'соль': {'order': 6, 'amount': []},
        'перец': {'order': 7, 'amount': []},
    }


def test_dict_to_ingredients():
    # GIVEN
    ingredients = '\n'.join((
        'яйца 4 шт',
        'сыр 50 г',
        'ветчина 2 кусочка',
        'брокколи 100 г',
        'помидор 1',
        'болгарский перец 1',
        'соль',
        'перец',
    ))
    print(ingredients)
    print('-' * 100)
    ingr_dict = subject.ingredients_to_dict(ingredients)

    # WHEN
    result = '\n'.join(subject.dict_to_ingredients(ingr_dict))
    # THEN
    print(result)
    assert result == '\n'.join((
        'яйца 4 шт',
        'сыр 50 г',
        'ветчина 2 кусоч',
        'брокколи 100 г',
        'помидор 1',
        'болгарский перец 1',
        'соль',
        'перец',
    ))


def test_get_ingredients_when_amounts_from_start():
    ingredients = """
    1 litre/2 pints chicken stock
    300ml/11fl oz water
    6 sticks lemongrass, lightly crushed
    4 fresh coriander roots, crushed
    110g/4oz 35 % fresh galangal, peeled and sliced (available from Asian supermarkets)
    8 tomatoes, cut into quarters, seeds removed
    6 kaffir lime leaves
    1-2 limes, juice only
    75ml/3fl oz tamarind water (tamarind is available from Asian supermarkets. Soak the tamarind in hot water and push the pulp through a sieve to make tamarind water.)
    3 red chillies, thinly sliced
    75ml/3fl oz fish sauce (nam pla), or to taste
    75g/3oz palm sugar (available from Asian supermarkets), use brown sugar if unavailable
    12 raw tiger prawns, shelled, gutted and split in half
    2 boneless skinless chicken breasts, cut into chunks

    0,5 ст. чечевицы белуга;
    125 гр. мягкого козьего сыра;
    хлеб (чиабатта);
    по 2 ст. л. оливкового масла и винного уксуса;
    1-2 зубчика чеснока;
    лук-резанец (или другая зелень);
    50 мл молока или сливок;
    соль,
    чёрный перец
    """
    # WHEN
    result = subject.ingredients_to_dict(ingredients)

    # THEN
    assert result == {
        'chicken stock': {'amount': [('1', 'litre'), ('2', 'pints')], 'order': 0},
        'water': {'amount': [('300', 'ml'), ('11', 'fl oz')], 'order': 1},
        'lemongrass, lightly crushed': {'amount': [('6', 'stick')], 'order': 2},
        'fresh coriander roots, crushed': {'amount': [('4', '')], 'order': 3},
        '35 % fresh galangal, peeled and sliced (available from Asian supermarkets)': {
            'amount': [('110', 'g'), ('4', 'oz')], 'order': 4
        },
        'tomatoes, cut into quarters, seeds removed': {'amount': [('8', '')], 'order': 5},
        'kaffir lime leaves': {'amount': [('6', '')], 'order': 6},
        'limes, juice only': {'amount': [('1', ''), ('2', '')], 'order': 7},

        'tamarind water (tamarind is available from Asian supermarkets.'
        ' Soak the tamarind in hot water and push the pulp through a sieve to make tamarind water.)': {
            'amount': [('75', 'ml'), ('3', 'fl oz')], 'order': 8},

        'red chillies, thinly sliced': {'amount': [('3', '')], 'order': 9},
        'fish sauce (nam pla), or to taste': {'amount': [('75', 'ml'), ('3', 'fl oz')], 'order': 10},
        'palm sugar (available from Asian supermarkets), use brown sugar if unavailable': {
            'amount': [('75', 'g'), ('3', 'oz')], 'order': 11
        },
        'raw tiger prawns, shelled, gutted and split in half': {'amount': [('12', '')], 'order': 12},
        'boneless skinless chicken breasts, cut into chunks': {'amount': [('2', '')], 'order': 13},
        'чечевицы белуга;': {'amount': [('0,5', 'ст.')], 'order': 15},
        'мягкого козьего сыра;': {'amount': [('125', 'гр.')], 'order': 16},
        'хлеб (чиабатта);': {'amount': [], 'order': 17},
        'по  оливкового масла и винного уксуса;': {'amount': [('2', 'ст. л.')], 'order': 18},
        'чеснока;': {'amount': [(['1', '2'], 'зубчик')], 'order': 19},
        'лук-резанец (или другая зелень);': {'amount': [], 'order': 20},
        'молока или сливок;': {'amount': [('50', 'мл')], 'order': 21},
        'соль,': {'amount': [], 'order': 22},
        'чёрный перец': {'amount': [], 'order': 23}
    }
