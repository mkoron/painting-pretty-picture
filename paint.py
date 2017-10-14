'''
Loads some data from an URL and draws a graph. The graph is saved as a
PDF file.
'''

import utils
import requests
import sys
from reportlab.graphics.shapes import Drawing, String, colors
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics import renderPDF

URL = 'http://services.swpc.noaa.gov/text/predicted-sunspot-radio-flux.txt'
COMMENT_CHARS = '#:'

colorHigh = colors.red
colorLow = colors.green
colorPred = colors.blue

drawing = Drawing(400, 300)
data = []
response = requests.get(URL)

if response.status_code != 200:
    print('Error fetching URL')
    sys.exit(1)

dataTable = response.text.strip()

for line in dataTable.split('\n'):
    if not line.isspace() and not line[0] in COMMENT_CHARS:
        data.append([float(num) for num in line.split()])

# Get data for graph
pred = [row[2] for row in data]
high = [row[3] for row in data]
low = [row[4] for row in data]
times = [row[0] + row[1] / 12 for row in data]

# Create graph
lp = LinePlot()
legend = Legend()

legend.colorNamePairs = [(colorPred, 'PREDICTED'),
                         (colorHigh, 'HIGH'), (colorLow, 'LOW')]
legend.x = 300
legend.y = 70
legend.fontName = 'Helvetica'
legend.fontSize = 8
lp.x = 50
lp.y = 100
lp.height = 125
lp.width = 300
lp.data = [list(zip(times, pred)), list(
    zip(times, high)), list(zip(times, low))]

lp.lines[0].strokeColor = colorPred
lp.lines[1].strokeColor = colorHigh
lp.lines[2].strokeColor = colorLow


# Since the year is a decimal we need to change the format
lp.xValueAxis.labelTextFormat = utils.formatter

# Draw graph
drawing.add(lp)
drawing.add(legend)
drawing.add(
    String(
        250,
        300,
        'Sunspots',
        fontsize=15,
        filegendColor=colors.grey))

# Create output PDF
renderPDF.drawToFile(drawing, 'report.pdf', 'Sunspots')
