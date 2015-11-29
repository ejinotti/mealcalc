from collections import defaultdict
from itertools import product, combinations

import sys

import database as db

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

        data[key].append(db.Meal(
            name=line[0],
            protein=float(line[1]),
            carbs=float(line[2]),
            fat=float(line[3]),
            calories=float(line[4]),
        ))

if not data['meals']:
    raise Exception('No meals in data file.')

db.destroy()
print 'DB cleared..'

db.create()

print 'Generating custom meals..'
for p in product(data['proteins'], data['carbs'], data['veggies']):
    data['meals'].append(db.Meal.from_parts(p))

num_meals = len(data['meals'])
num_combos = (num_meals * (num_meals-1) * (num_meals-2) / 6) * \
    len(data['breakfasts'])

print '{} meals.'.format(num_meals)
print '{} days to generate.'.format(num_combos)

print 'Generating days..'
days = []
i = 0
for c in combinations(data['meals'], 3):
    for b in data['breakfasts']:
        meals = (b,) + c
        d = db.Day(**db.Meal.combine(meals, with_name=False))

        for m in meals:
            d.meals.append(m)

        days.append(d)

        i += 1
        print '\r{}'.format(i),

print 'Adding meals..'
db.session.add_all(data['meals'] + data['breakfasts'])

print 'Adding days..'
db.session.add_all(days)

print 'Commit..'
db.session.commit()
