import datetime as dt
import json
import logging
import os

import pandas as pd

from flask import current_app


def get_forecast_dates(date_dir_format: str = "%Y-%m-%d"):
    """

    :param date_dir_format:
    :return:
    """
    data_path = current_app.config.get("DATA_PATH")
    logging.info("Looking for forecast dates in {}".format(data_path))

    data_directory = os.walk(data_path)
    _, data_types, _ = next(data_directory)

    forecast_dates = list()
    for _, date_dirs, _ in data_directory:
        for d in date_dirs:
            try:
                if dt.datetime.strptime(d, date_dir_format):
                    forecast_dates.append(d)
            except ValueError:
                logging.warning("{} does not match format string {}, not including directory".
                                format(d, date_dir_format))

    return list(set(forecast_dates))


def get_forecast_data(lookup_date: dt.date = None,
                      date_dir_format: str = "%Y-%m-%d"):
    """

    :param lookup_date:
    :param date_dir_format:
    :return:
    """
    icenet_data = current_app.config.get("DATA_PATH")
    data_directory = os.walk(icenet_data)
    _, data_types, _ = next(data_directory)

    forecast_dates = get_forecast_dates(date_dir_format)

    if len(forecast_dates) == 0:
        return None

    if lookup_date is not None:
        logging.info("Looking for data specifically on {}".format(lookup_date.strftime("%F")))
        forecast_dates = [date_dir for date_dir in forecast_dates
                          if lookup_date.strftime(date_dir_format) == date_dir]

    logging.debug("Data types: {}".format(data_types))
    logging.debug("Forecast date directories available: {}".format(forecast_dates))

    inventory = {filename: os.path.join(icenet_data, data_type, forecast_date, filename)
                 for forecast_date in forecast_dates
                 for data_type in data_types
                 for filename in os.listdir(os.path.join(icenet_data, data_type, forecast_date))}
    return inventory


def load_json(filename, icenet_data_inventory=None):
    if not icenet_data_inventory:
        icenet_data_inventory = get_forecast_data()

    try:
        file_path = icenet_data_inventory[filename]
    except KeyError:
        logging.warning("We're missing a file: {}".format(filename))
        return None

    logging.debug("Attempting to load {}".format(file_path))

    file_size = os.stat(file_path).st_size
    if file_size > 1024 ** 2:
        return dict(error="File is too large: {}kB".format(file_size / 1024))

    try:
        with open(file_path, "r") as fh:
            return json.load(fh)
    except json.JSONDecodeError as e:
        logging.exception("JSON decoding error: {}".format(e.msg))
        return dict(error="JSON decoding error: no data available...")
