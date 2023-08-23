import datetime as dt
import logging
import os
from urllib.parse import urlparse

import pandas as pd
from bas_style_kit_jinja_templates import BskTemplates
from flask import redirect, render_template, request
from jinja2 import PrefixLoader, PackageLoader

import connexion

logging.getLogger().setLevel(logging.DEBUG)

from icenet_app.plots import line_plot
from icenet_app.utils import load_json, get_forecast_data


def create_app(config_class=None):
    connexion_app = connexion.FlaskApp(__name__,
                                       specification_dir="../")
    connexion_app.add_api("swagger.yml")
    application = connexion_app.app

    if config_class is not None:
        application.config.from_object(config_class)

    application.jinja_loader = PrefixLoader({
        "app": PackageLoader("icenet_app"),
        "bas_style_kit": PackageLoader('bas_style_kit_jinja_templates'),
    })
    application.config['BSK_TEMPLATES'] = BskTemplates()
    application.config['BSK_TEMPLATES'].bsk_site_nav_brand_text = 'IceNet'
    application.config['BSK_TEMPLATES'].bsk_site_development_phase = 'alpha'
    application.config['BSK_TEMPLATES'].bsk_site_feedback_href = '/feedback'
    application.config['BSK_TEMPLATES'].bsk_site_footer_policies_cookies_href = '/legal/cookies'
    application.config['BSK_TEMPLATES'].bsk_site_footer_policies_copyright_href = '/legal/copyright'
    application.config['BSK_TEMPLATES'].bsk_site_footer_policies_privacy_href = '/legal/privacy'
    application.config['BSK_TEMPLATES'].site_description = 'IceNet Dashboard and API services'
    application.config['BSK_TEMPLATES'].site_styles.append({'href': '/static/css/main.css'})
    application.config['BSK_TEMPLATES'].site_title = 'IceNet Dashboard'

    return application


app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("app/errors/404.j2"), 404


@app.route('/')
def index():
    service = urlparse(request.base_url).netloc.split(":")[0].split(".")[0]

    if service == "api":
        location = "{}api/ui".format(request.base_url)
        logging.info("Redirecting to the API at {}".format(location))
        return redirect(location, 301)

    inventory = get_forecast_data()
    icenet_metadata = load_json("output_metadata.json", icenet_data_inventory=inventory)

    date_range_files = sorted([df.split(".")[0] for df in inventory.keys() if df.endswith(".png")])
    if len(date_range_files) < 1:
        logging.warning("No image data available")
    else:
        date_range = pd.date_range(date_range_files[0], date_range_files[-1])

        icenet_metadata.update(dict(
            date_range=date_range,
            init_date=(date_range[0] - dt.timedelta(days=1)).strftime("%F"),
            end_date=date_range[-1].strftime("%F"),
            start_date=date_range[0].strftime("%F"),
        ))

    return render_template("app/index.j2",
                           icenet_metadata=icenet_metadata,
                           icenet_sie_change=line_plot(load_json("output_sie_growth.json",
                                                                 icenet_data_inventory=inventory),
                                                       title="Sea ice extent change"),
                           icenet_trend_mean=line_plot(load_json("output_trend.json",
                                                                 icenet_data_inventory=inventory)['mean'],
                                                       title="Sea ice mean change"),
                           icenet_trend_stddev=line_plot(load_json("output_trend.json",
                                                                   icenet_data_inventory=inventory)['stddev'],
                                                         title="Ensemble stddev change"))
