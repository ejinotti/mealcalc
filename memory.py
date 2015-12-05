#!/usr/bin/env python

from collections import defaultdict, namedtuple
from itertools import product, combinations

import time
import sys


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

print '\nenter calories:',
targ = float(raw_input())
print '\nenter tolerance:',
tol = float(raw_input())
print '\nenter ratio p/c/f (space sep):',
ratio = map(float, raw_input().split())
print '\nenter ratio tolerance (pct pts):',
ratio_tol = float(raw_input())

c_min = targ - tol
c_max = targ + tol

ratio = [(r - ratio_tol, r + ratio_tol) for r in ratio]

results = []

print '\ncalculating..'
t0 = time.time()

for c in combinations(data['meals'], 3):
    for b in data['breakfasts']:
        meals = (b,) + c

        stats = Meal.sum_stats(meals)

        if not c_min < stats['calories'] < c_max:
            continue

        stats['protein_pct'] = stats['protein'] * 400.0 / stats['calories']
        if not ratio[0][0] < stats['protein_pct'] < ratio[0][1]:
            continue

        stats['carbs_pct'] = stats['carbs'] * 400.0 / stats['calories']
        if not ratio[1][0] < stats['carbs_pct'] < ratio[1][1]:
            continue

        stats['fat_pct'] = stats['fat'] * 900.0 / stats['calories']
        if not ratio[2][0] < stats['fat_pct'] < ratio[2][1]:
            continue

        for i, m in enumerate(meals, start=1):
            stats['meal' + str(i)] = str(m)

        results.append(stats)

print '\nfound {} results in {}s.\n'.format(
    len(results), round(time.time() - t0, 1))

print '\n\n'.join([str(r) for r in results[0:10]])
