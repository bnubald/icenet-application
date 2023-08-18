import requests

from bokeh.plotting import figure, curdoc
from bokeh.resources import CDN
from bokeh.embed import file_html

import numpy as np

TOOLS = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo," \
        "reset,tap,save,box_select,poly_select,lasso_select,examine,help"


def line_plot(data, title):
    p = figure(title=title, tools=TOOLS, width=500, height=300)
    p.line(list(data.keys()), list(data.values()))
    html = file_html(p, CDN, "my plot")
    return html

