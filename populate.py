#!/usr/bin/env python

from collections import defaultdict, namedtuple
from itertools import product, combinations

import time

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

print 'Generating custom meals..'
for p in product(data['proteins'], data['carbs'], data['veggies']):
    data['meals'].append(Meal.combine(p))

num_meals = len(data['meals'])
num_combos = (num_meals * (num_meals-1) * (num_meals-2) / 6) * \
    len(data['breakfasts'])

print '{} meals.'.format(num_meals)
print '{} days to generate.'.format(num_combos)

total = 0
batch = 100000

conn = db.clear_and_get_sqlite()
cur = conn.cursor()
cols = db.Day.__mapper__.columns.keys()[1:]
statement = 'INSERT INTO days ({}) VALUES ({})'.format(
    ', '.join(cols),
    ', '.join([c for c in ('?' * len(cols))])
)

print 'Generating days..'
days = []
t0 = time.time()

for c in combinations(data['meals'], 3):
    for b in data['breakfasts']:
        meals = (b,) + c
        stats = Meal.sum_stats(meals)

        vals = (
            stats['calories'],
            stats['protein'],
            stats['carbs'],
            stats['fat'],
            stats['protein'] * 400.0 / stats['calories'],
            stats['carbs'] * 400.0 / stats['calories'],
            stats['fat'] * 900.0 / stats['calories'],
            str(meals[0]),
            str(meals[1]),
            str(meals[2]),
            str(meals[3]),
        )

        days.append(vals)

        if len(days) >= batch:
            cur.executemany(statement, days)

            total += len(days)
            days = []
            print total

if days:
    cur.executemany(statement, days)
    total += len(days)

conn.commit()

print 'Inserted {} in {}s. Batches of {}.'.format(
    total, round(time.time() - t0, 1), batch)

print 'Done.'
