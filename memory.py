#!/usr/bin/env python

from collections import defaultdict
from itertools import product, combinations

import time


class Item(object):
    def __init__(self, *args):
        if isinstance(args[0], Item):
            self.name = args[0].name
            self.protein = args[0].protein
            self.carbs = args[0].carbs
            self.fat = args[0].fat
            self.calories = args[0].calories

            for arg in args[1:]:
                self.add(arg)

        else:
            self.name = args[0]
            self.protein = float(args[1])
            self.carbs = float(args[2])
            self.fat = float(args[3])
            self.calories = float(args[4])

    def __repr__(self):
        return '{}\n{}p {}c {}f {}cal'.format(
            self.name,
            self.protein,
            self.carbs,
            self.fat,
            self.calories,
        )

    def add(self, item):
        self.name += ' + {}'.format(item.name)
        self.protein += item.protein
        self.carbs += item.carbs
        self.fat += item.fat
        self.calories += item.calories


class Day(object):
    def __init__(self, items):
        self.calories = reduce(lambda x, i: x + i.calories, items, 0)
        self.items = items

    def in_tolerance(self, c_min, c_max):
        return c_min < self.calories < c_max

    def _calc_pcts(self):
        self.protein = reduce(lambda x, i: x + i.protein, self.items, 0)
        self.carbs = reduce(lambda x, i: x + i.carbs, self.items, 0)
        self.fat = reduce(lambda x, i: x + i.fat, self.items, 0)

        self.protein_pct = round(self.protein * 400.0 / self.calories, 1)
        self.carbs_pct = round(self.carbs * 400.0 / self.calories, 1)
        self.fat_pct = round(self.fat * 900.0 / self.calories, 1)

    def in_ratio(self, ratio):
        self._calc_pcts()

        return (
            ratio[0][0] < self.protein_pct < ratio[0][1]
            and
            ratio[1][0] < self.carbs_pct < ratio[1][1]
            and
            ratio[2][0] < self.fat_pct < ratio[2][1]
        )

    def __repr__(self):
        return ('Day: {} total calories.\n'
                'Macros: {}g protein {}g carb {}g fat.\n'
                'Ratio: {}% protein {}% carb {}% fat.\n'
                '{}'.format(
                    self.calories,
                    self.protein, self.carbs, self.fat,
                    self.protein_pct, self.carbs_pct, self.fat_pct,
                    '\n'.join([str(i) for i in self.items]),
                ))


meals = []
parts = defaultdict(list)
breakfasts = []

with open('fueldata.txt', 'r') as f:
    buff = meals

    for line in (l.strip() for l in f):
        if not line:
            continue

        line = line.split(',')

        if len(line) == 1:
            if line[0] == 'breakfast meals':
                buff = breakfasts
            elif line[0] == 'signature':
                buff = meals
            elif line[0] == 'breakfast':
                buff = None
            else:
                buff = parts[line[0]]

            continue

        if buff is None:
            continue

        buff.append(Item(*line))

for p in product(parts['meats'], parts['carbs'], parts['veggies']):
    meals.append(Item(*p))

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

for d in combinations(meals, 3):
    for b in breakfasts:
        day = Day((b,) + d)

        if day.in_tolerance(c_min, c_max) and day.in_ratio(ratio):
            results.append(day)

print '\nfound {} results in {}s.\n'.format(
    len(results), round(time.time() - t0, 1))

print '\n\n'.join([str(r) for r in results[0:10]])
