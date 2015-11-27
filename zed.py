from collections import defaultdict


class Item(object):
    def __init__(self, name, p, c, f, cal):
        self.name = name
        self.protein = p
        self.carbs = c
        self.fat = f
        self.calories = cal

    def __repr__(self):
        return '{}\n{}p {}c {}f {}cal'.format(
            self.name,
            self.protein,
            self.carbs,
            self.fat,
            self.calories,
        )

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

    print 'meals'
    for m in meals:
        print m

    print '\nmeats'
    for m in parts['meats']:
        print m

    print '\ncarbs'
    for c in parts['carbs']:
        print c

    print '\nveggies'
    for v in parts['veggies']:
        print v

    print '\nbreakfast meals'
    for b in breakfasts:
        print b
