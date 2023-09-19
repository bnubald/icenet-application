import datetime as dt
import logging
import numpy as np
import os

import pandas as pd
import xarray as xr

from flask import jsonify, send_file

from icenet_app.utils import get_forecast_data


def get_image_data(forecast_date: str,
                   leadtime: int = 1,
                   data_type: str = "sic_mean",
                   region: tuple = (0, 0, 432, 432)):
    icenet_data = os.environ["ICENET_DATA_LOCATION"] \
        if "ICENET_DATA_LOCATION" in os.environ else os.path.join(".", "data")

    ds = xr.open_dataset(os.path.join(icenet_data, "north_daily_forecast.{}_north.nc".format(forecast_date)))

    da = ds.isel(time=0, leadtime=int(leadtime))
    pred_data = getattr(da, data_type).to_numpy()

    x1, y1, x2, y2 = region
    pred_data = pred_data[(len(ds.yc) - y2):(len(ds.yc) - y1), x1:x2]

    return pred_data.tolist()


def get_image(forecast_date: str,
              image: str):
    inventory = get_forecast_data(pd.to_datetime(forecast_date))
    return send_file(inventory[image], mimetype='image/png')


def get_version():
    return jsonify("0.1.0")
