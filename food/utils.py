import re
from typing import List, Tuple

UNITS = [
    r'ст л\b', r'ст\b', r'гр', r'г\b', r'зубчик', r'щепотка', r'шт\b', r'мл\b', r'кусоч',
    r'litre', r'\bl\b', r'ml\b', r'fl oz', r'stick', r'g\b', r'oz\b', r'pints',
]


def wrap(u):
    return '\s+'.join(f'{p}\.?' for p in u.split())


UNIT_PATTERN = re.compile(r'(?P<unit>' + '|'.join([wrap(u) for u in UNITS]) + ')')


def ingredients_to_dict(s: str) -> dict:
    if not s:
        return {}
    result = {}
    for i, line in enumerate(s.strip().splitlines()):
        if not line.strip():
            continue
        units = get_ingredient_unit(line)
        amounts = get_ingredient_amount(line, units)
        title = get_ingredient(line, amounts).strip()
        result[title] = {'amount': amounts, 'order': i}

    return result


def get_ingredient(line: str, amount_to_unit: List[Tuple[str, str]]) -> str:
    if not amount_to_unit:
        return line
    pattern = r'\W+'.join(get_amount_pattern(a, u) for a, u in amount_to_unit) + '\S*'
    return re.sub(pattern, '', line).strip()


def get_amount_pattern(a: str or list, u: str):
    if isinstance(a, list):
        return '\s*-\s*'.join(a) + '\s*' + u
    return f'{a}\W*{u}\S*' if a and u else a


def get_ingredient_amount(line: str, units) -> List[Tuple[str, str]] or List[Tuple[List[str], str]]:
    numbers = re.findall(r"\d*[,.\\]\d+|\d+", line)

    if len(numbers) == len(units):
        return list(zip(numbers, units))
    elif not units and numbers:
        return list(zip(numbers, [''] * len(numbers)))

    if units:
        ln = re.sub(r'\W', '', line)
        amounts = [n for n in numbers for u in units if n + u in ln]
        if len(amounts) < len(numbers):
            amounts = [n for n in numbers for a in amounts for u in units if n + a + u in ln] + amounts

        if len(units) == len(amounts):
            return list(zip(amounts, units))
        else:
            return [(amounts, units[0])]


def get_ingredient_unit(line: str) -> List[str]:
    return UNIT_PATTERN.findall(line)


def dict_to_ingredients(d: dict) -> List[str]:
    items = sorted(d.items(), key=lambda ingredient: ingredient[1]['order'])
    result = []
    for title, amount_dict in items:
        t = [amounts_to_str(a) for a in amount_dict['amount']]
        result.append(' '.join([title, '/'.join(t)]).strip())
    return result


def amounts_to_str(amounts: list) -> (str, str):
    if not amounts:
        return ''
    a = '-'.join(amounts[0]) if type(amounts[0]) in (list, tuple) else amounts[0]

    return f'{a} {amounts[1]}'.strip()
