import database as db

while True:
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





# ratio = [(r - ratio_tol, r + ratio_tol) for r in ratio]
#
# results = []
#
# print '\ncalculating..'
#
# for d in combinations(meals, 3):
#     for b in breakfasts:
#         day = Day((b,) + d)
#
#         if day.in_tolerance(c_min, c_max) and day.in_ratio(ratio):
#             results.append(day)
#
# print '\nfound {} results.\n'.format(len(results))
#
# print '\n\n'.join([str(r) for r in results[0:10]])
