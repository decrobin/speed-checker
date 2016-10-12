# -*- coding: utf-8 -*-
import pygal
from flask import Flask, Response
import psycopg2


app = Flask(__name__)


@app.route('/')
def index():
    """ render svg on html """
    return """
<html>
    <body>
        <h1>hello pygal</h1>
        <figure>
        <embed type="image/svg+xml" src="/graph/" />
        </figure>
    </body>
</html>'
"""


@app.route('/graph/')
def graph():
    """
    Connect to postgres, get data, graph it, return it via template.
    """
    try:
        conn = psycopg2.connect("dbname='speed' user='speed' host='postgres'")
    except Exception, e:
        return str(e)
    # get db results, take this out into new function
    title = "Speed Test Results"
    cursor = conn.cursor()
    speed_results_query = """SELECT * FROM speed_results
    ORDER BY date ASC, time ASC
    ;"""
    cursor.execute(speed_results_query)
    rows = cursor.fetchall()
    datetimes = []
    pings = []
    downloads = []
    uploads = []
    for row in rows:
        datetimes.append(row[1] + row[2])
        pings.append(float(row[3]))
        downloads.append(float(row[4]))
        uploads.append(float(row[5]))

    # create a bar chart
    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = datetimes
    line_chart.add('Download', downloads)
    line_chart.add('Upload', uploads)
    return Response(response=line_chart.render(), content_type='image/svg+xml')


if __name__ == '__main__':
    app.run(host='0.0.0.0')