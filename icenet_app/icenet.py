import datetime as dt

import pandas as pd
from flask import jsonify, send_file

from icenet_app.utils import get_forecast_data


def get_image(forecast_date: str,
              image: str):
    inventory = get_forecast_data(pd.to_datetime(forecast_date))
    return send_file(inventory[image], mimetype='image/png')


def get_version():
    return jsonify("0.1.0")
