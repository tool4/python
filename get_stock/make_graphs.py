#import plotly
import plotly.graph_objects as go
import pandas as pd
import sys
import re
import os
import fnmatch

overwrite = False
if len(sys.argv) > 1:
    if sys.argv[1] == '-o':
        overwrite = True

pattern0 = "*.csv"
folder = '.'

def make_graph(root, filename, fileprefix, column):
    full_path = os.path.join(root, filename)
    output_filename = fileprefix + filename[:-4] + '.html'
    output_full_path = os.path.join(root, output_filename)
    if not os.path.isfile(output_full_path) or overwrite:
        print(filename + ' --> ' + output_filename)
        df = pd.read_csv(full_path)
        fig = go.Figure([go.Scatter(x=df['TIME'], y=df[column])])
        fig.write_html(output_full_path)

for root, dirs, files in os.walk(folder):
    for filename in files:
        if fnmatch.fnmatch(filename, pattern0):
            if filename != 'sp500.csv':
                make_graph(root, filename, "price_", " PRICE")
                make_graph(root, filename, "change_", " CHANGE")
                make_graph(root, filename, "changeperc_", " CHANGE_PERCENT")
