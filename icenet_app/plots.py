import requests

from bokeh.plotting import figure, curdoc
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.io import show
from bokeh.models import CustomJS, DateSlider

import numpy as np
import pandas as pd

# hover,crosshair,pan,undo,redo,
TOOLS = "wheel_zoom,zoom_in,zoom_out,box_zoom,reset,box_select,poly_select,lasso_select,examine,help"


def date_picker(date_range):
    date_slider = DateSlider(value=date_range[0].date(),
                             start=date_range[0].date(),
                             end=date_range[-1].date())
    date_slider.js_on_change("value", CustomJS(code="""
        let date = new Date(this.value);
        let month = date.getMonth() + 1;
        let monthStr = month < 10 ? "0" + month: month;
        let dayStr = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
        let dateStr = "".concat(date.getFullYear(), monthStr, dayStr);
        console.log("Showing " + dateStr);
        $("img#fc_image_sic_" + fc_image_cur_id).hide();
        $("img#fc_image_stddev_" + fc_image_cur_id).hide();
        $("img#fc_image_sic_" + dateStr).show();
        $("img#fc_image_stddev_" + dateStr).show();
        fc_image_cur_id = dateStr;
    """))

    return file_html(date_slider, CDN, "my slider")


def line_plot(data, title):
    p = figure(title=title, tools=TOOLS, width=500, height=300)
    p.line(list(data.keys()), list(data.values()))
    html = file_html(p, CDN, "my plot")
    return html

