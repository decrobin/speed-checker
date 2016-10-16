# -*- coding: utf-8 -*-
import pygal
from pygal.style import DefaultStyle
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

def get_speed_results_count(cursor):
    speed_results_query = """SELECT COUNT(*) FROM speed_results
    ;"""
    cursor.execute(speed_results_query)
    row = cursor.fetchone()
    return row


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
    cursor = connect_to_db()
    result = get_speed_results(cursor)
    count = get_speed_results_count(cursor)
    # if result is None:
    #     return ''
    datetimes = []
    downloads = []
    uploads = []
    pings = []
    for row in result:
        datetimes.append(row[1] + " " + row[2])
        pings.append(float(row[3]))
        downloads.append(float(row[4]))
        uploads.append(float(row[5]))
    
    num_labels = count[0] // 20
    
    # create a bar chart
    line_chart = pygal.Line(x_label_rotation=90, style=DefaultStyle, x_labels_major_every=num_labels, show_minor_x_labels=False, show_dots=False)
    line_chart.title = "Speed test results"
    line_chart.x_labels = datetimes
    line_chart.add('Download (Mbit/s)', downloads)
    line_chart.add('Upload (Mbit/s)', uploads)
    line_chart.add('Latency (ms)', pings, secondary=True)

    return Response(response=line_chart.render(), content_type='image/svg+xml')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
