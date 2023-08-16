import datetime
import requests
import json

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, json_item

import numpy as np


def default_plot():
    N = 4000
    x = np.random.random(size=N) * 100
    y = np.random.random(size=N) * 100
    radii = np.random.random(size=N) * 1.5
    colors = np.array([(r, g, 150) for r, g in zip(50 + 2 * x, 30 + 2 * y)], dtype="uint8")
    TOOLS = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,examine,help"

    plot = figure(tools=TOOLS, height=300, width=500)

    plot.scatter(x, y, radius=radii,
              fill_color=colors, fill_alpha=0.6,
              line_color=None)

    html = file_html(plot, CDN, "my plot")
    #json_embed = json.dumps(json_item(plot, "myplot"))
    #return json_embed
    return html

def geoapi_plot():
    api_base_url = "https://app-icenetuat-pygeoapi.azurewebsites.net/"
    response = requests.get(f"{api_base_url}/collections/north_forecasts_latest/items?bbox=-10,40,10,80&limit=1000/sea_ice_concentration_mean")