from collections import defaultdict, namedtuple
from itertools import product, combinations

import sys

import database as db


class Meal(namedtuple('Meal', 'name protein carbs fat calories')):
    __slots__ = ()

    @classmethod
    def sum_stats(cls, meals):
        stats = defaultdict(int)

        for m in meals:
            stats['protein'] += m.protein
            stats['carbs'] += m.carbs
            stats['fat'] += m.fat
            stats['calories'] += m.calories

        return stats

    @classmethod
    def combine(cls, meals):
        name = ' + '.join([m.name for m in meals])
        return cls(name=name, **cls.sum_stats(meals))

    def __repr__(self):
        return '{}\n{}p {}c {}f {}cal'.format(*vars(self).values())

if len(sys.argv) != 2:
    raise Exception('Must give exactly one arg (data file name).')

data = defaultdict(list)

with open(sys.argv[1], 'r') as f:
    key = 'meals'

    for line in (l.strip() for l in f):
        if not line:
            continue

        line = line.split(',')

        if len(line) == 1:
            key = line[0]
            continue

        data[key].append(Meal(line[0], *map(float, line[1:])))

if not data['meals']:
    raise Exception('No meals in data file.')

db.destroy()
print 'DB cleared..'

db.create()

print 'Generating custom meals..'
for p in product(data['proteins'], data['carbs'], data['veggies']):
    data['meals'].append(Meal.combine(p))

num_meals = len(data['meals'])
num_combos = (num_meals * (num_meals-1) * (num_meals-2) / 6) * \
    len(data['breakfasts'])

print '{} meals.'.format(num_meals)
print '{} days to generate.'.format(num_combos)

print 'Generating days..'
days = []
for c in combinations(data['meals'], 3):

    for b in data['breakfasts']:
        meals = (b,) + c
        day = Meal.sum_stats(meals)

        day['protein_pct'] = round(day['protein'] * 4.0 / day['calories'], 1)
        day['carbs_pct'] = round(day['carbs'] * 4.0 / day['calories'], 1)
        day['fat_pct'] = round(day['fat'] * 9.0 / day['calories'], 1)

        for i, m in enumerate(meals):
            day['meal' + str(i + 1)] = str(m)

        days.append(day)

    if len(days) > 10000:
        break

print 'Done generating.. Inserting..'
db.engine.execute(db.Day.__table__.insert(), days)

print 'Done inserting.'
