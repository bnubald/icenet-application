import datetime as dt
import json
import logging
import os
from urllib.parse import urlparse

import pandas as pd

from bas_style_kit_jinja_templates import BskTemplates
from bokeh.resources import CDN
from flask import redirect, render_template, request
from jinja2 import PrefixLoader, PackageLoader
from werkzeug.security import generate_password_hash, check_password_hash

import connexion

from icenet_app.config import configs
from icenet_app.extensions import auth
from icenet_app.plots import plots
from icenet_app.utils import load_json, get_forecast_data

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("connexion").setLevel(logging.INFO)
logging.getLogger("werkzeug").setLevel(logging.WARNING)


def create_app():
    config_class = configs[os.getenv("ICENET_APP_ENV") or "production"]
    logging.info("Loading from configuration class: {}".format(config_class))

    connexion_app = connexion.FlaskApp(__name__,
                                       specification_dir=config_class.SWAGGER_SPECIFICATION_DIR)
    connexion_app.add_api(config_class.SWAGGER_SPECIFICATION)
    application = connexion_app.app

    config_class.init_app(application)
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

    application.register_blueprint(plots, url_prefix='/plots')
    #logging.info(application.url_map)

    return application


app = create_app()


@app.before_request
@auth.login_required
def ensure_authorised():
    pass


@auth.verify_password
def verify_password(username, password):
    user_list = app.config['USERS']
    auth_file = os.getenv("ICENET_AUTH_LIST") or None
    auth_entry = os.getenv("ICENET_AUTH_USER") or None

    if auth_file is not None:
        with open(auth_file, "r") as fh:
            users = json.load(fh)
            user_list.update({
                k: generate_password_hash(v) for k, v in users.items()
            })

    if auth_entry is not None:
        user_list.update({
            auth_entry.split(":")[0]: generate_password_hash(auth_entry.split(":")[1])
        })

    if username in user_list and check_password_hash(user_list[username], password):
        return username


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

    if inventory is None:
        logging.warning("No data is available")
        return render_template("app/index.j2",
                               bokeh_resources=None,
                               icenet_metadata=None)
    icenet_metadata = load_json("output_metadata.json", icenet_data_inventory=inventory)

    date_range_files = sorted([df.split(".")[1] for df in inventory.keys() if df.endswith(".png")])
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

    logging.info(app.config["USERS"])
    return render_template("app/index.j2",
                           bokeh_resources=CDN.render(),
                           icenet_metadata=icenet_metadata)
