#!/usr/bin/env python

import time

import database as db

s = db.get_orm_session()

while True:
    print '\nenter calories:',
    targ = float(raw_input())
    print '\nenter calorie tolerance:',
    c_tol = float(raw_input())
    print '\nenter ratio p/c/f (space sep):',
    ratio = map(float, raw_input().split())
    print '\nenter ratio tolerance (pct pts):',
    r_tol = float(raw_input())

    cals_min = targ - c_tol
    cals_max = targ + c_tol

    p_min = ratio[0] - r_tol
    p_max = ratio[0] + r_tol

    c_min = ratio[1] - r_tol
    c_max = ratio[1] + r_tol

    f_min = ratio[2] - r_tol
    f_max = ratio[2] + r_tol

    q = s.query(db.Day).filter(db.expression.and_(
        db.expression.between(db.Day.calories, cals_min, cals_max),
        db.expression.between(db.Day.protein_pct, p_min, p_max),
        db.expression.between(db.Day.carbs_pct, c_min, c_max),
        db.expression.between(db.Day.fat_pct, f_min, f_max),
    ))

    print '\ncalories {} ~ {}'.format(cals_min, cals_max)
    print 'protein_pct {}% ~ {}%'.format(p_min, p_max)
    print 'carbs_pct {}% ~ {}%'.format(c_min, c_max)
    print 'fat_pct {}% ~ {}%'.format(f_min, f_max)
    print '\nquerying..'

    t0 = time.time()
    results = q.all()
    print 'Found {} results in {}s.'.format(
        len(results), round(time.time() - t0, 1))

    print 'Show results? (y/n):',
    if raw_input().lower() == 'y':
        print '\n'.join([str(d) for d in results])
