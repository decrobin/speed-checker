# -*- coding: utf-8 -*-
import pygal
from pygal.style import DarkStyle
from flask import Flask, Response
import psycopg2


app = Flask(__name__)


def connect_to_db():
    try:
        conn = psycopg2.connect("dbname='speed' user='speed' host='speed-checker-postgres'")
    except Exception:
        return None
    # get db results, take this out into new function
    cursor = conn.cursor()
    return cursor


def get_speed_results(cursor):
    # if cursor is None:
    #     return None
    speed_results_query = """SELECT * FROM speed_results
    ORDER BY date ASC, time ASC
    ;"""
    cursor.execute(speed_results_query)
    rows = cursor.fetchall()
    return rows


@app.route('/')
def index():
    """ render svg on html """
    return """
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
    </head>
    <body style="margin:10%,padding=10%">
        <figure>
        <embed type="image/svg+xml" src="/speed/" />
        </figure>
        <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
    </body>
</html>'
"""


@app.route('/speed/')
def speed():
    """
    Connect to postgres, get data, graph it, return it via template.
    """
    result = get_speed_results(connect_to_db())
    # if result is None:
    #     return ''
    print result


if __name__ == '__main__':
    speed()
