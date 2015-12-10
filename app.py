#!/usr/bin/env python

from flask import Flask, render_template
from collections import namedtuple, defaultdict


app = Flask(__name__, static_url_path='/public')

Item = namedtuple('Item', 'name protein carbs fat calories')


def readfile(f):
    data = defaultdict(list)
    key = 'meals'

    for line in (l.strip() for l in f):
        if not line:
            continue

        line = line.split(',')

        if len(line) == 1:
            key = line[0]
            continue

        data[key].append(Item(*line))

    return data


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    with app.open_resource('fueldata.txt', 'r') as f:
        data = readfile(f)

    return render_template('./index.html', **data)


app.run(debug=True)
