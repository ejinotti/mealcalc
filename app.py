#!/usr/bin/env python

from flask import Flask, render_template, send_from_directory
from collections import namedtuple, defaultdict


app = Flask(__name__)

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


@app.route('/')
def index():
    with app.open_resource('fueldata.txt', 'r') as f:
        data = readfile(f)

    return render_template('./index.html', **data)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


app.run(debug=True)
