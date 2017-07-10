import re
from typing import List, Tuple

UNITS = [
    r'ст л', r'ст', r'гр', r'г\b', r'зубчик', r'шт', r'мл', r'кусоч',
    r'litre', r'\bl\b', r'ml', r'fl oz', r'stick', r'g\b', r'oz', r'pints',
]


def wrap(u):
    return ' '.join(f'{p}\.?' for p in u.split())


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
            # r = []
            # for u in units:
            #     tmp = []
            #     for a in reversed(amounts):
            #         if ''.join(tmp) + a + u in ln:
            #             tmp.insert(0, a)
            #     r.append((tmp, u))
            # if 'зубчик' in units:
            #     print(amounts, r)
            return [(amounts, units[0])]


def get_ingredient_unit(line: str) -> List[str]:
    return UNIT_PATTERN.findall(line)


def dict_to_ingredients(d: dict) -> List[str]:
    items = sorted(d.items(), key=lambda ingredient: ingredient[1]['order'])
    result = []
    for title, d in items:
        t = [amounts_to_str(a) for a in d['amount']]
        result.append(' '.join([title, '/'.join(t)]).strip())
    return result


def amounts_to_str(amounts: list) -> (str, str):
    if not amounts:
        return ''

    a = '-'.join(amounts[0]) if isinstance(amounts[0], tuple) else amounts[0]

    return f'{a} {amounts[1]}'.strip()
