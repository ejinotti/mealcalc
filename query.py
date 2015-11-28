from collections import defaultdict
from itertools import product, combinations


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
            if line[0] == 'breakfasts':
                buff = breakfasts
            elif line[0] == 'meals':
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

for d in combinations(meals, 3):
    for b in breakfasts:
        day = Day((b,) + d)

        if day.in_tolerance(c_min, c_max) and day.in_ratio(ratio):
            results.append(day)

print '\nfound {} results.\n'.format(len(results))

print '\n\n'.join([str(r) for r in results[0:10]])
