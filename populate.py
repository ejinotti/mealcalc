from collections import defaultdict
from itertools import product

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

for m in data['meals']:
    db.session.add(m)

for p in product(data['proteins'], data['carbs'], data['veggies']):
    db.session.add(db.Meal.from_parts(p))

print 'len new = {}'.format(len(db.session.new))

db.session.commit()
