from collections import defaultdict
from itertools import product


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

    for combo in product(parts['meats'], parts['carbs'], parts['veggies']):
        meals.append(Item(*combo))

    print 'meals'
    for m in meals:
        print m

    print '\nbreakfast meals'
    for b in breakfasts:
        print b

    # print '\nenter calories:',
    # target_cals = float(raw_input())
    # print '\nenter tolerance:',
    # tolerance = float(raw_input())
