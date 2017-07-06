import re


def get_ingredients(s: str) -> dict:
    p = re.compile(r'(?P<not_title>(?P<amount>\d+)(\s+(?P<unit>[^\d]+))?)$')
    result = {}
    for i, line in enumerate(s.strip().splitlines()):
        match = p.search(line.strip())
        if match:
            groups = match.groupdict()
            title = line.replace(groups['not_title'], '')
            amount = groups['amount']
            unit = groups.get('unit')
        else:
            title = line
            amount = None
            unit = None

        result[title.strip()] = {'amount': amount, 'unit': unit, 'order': i}

    return result
