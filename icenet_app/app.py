import logging
import os
from urllib.parse import urlparse

from bas_style_kit_jinja_templates import BskTemplates
from flask import redirect, render_template, request
from jinja2 import PrefixLoader, PackageLoader, FileSystemLoader

import connexion

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("connexion").setLevel(logging.DEBUG)


def create_app(config_class=None):
    connexion_app = connexion.FlaskApp(__name__,
                             specification_dir="../")
    connexion_app.add_api("swagger.yml")
    app = connexion_app.app

    if config_class is not None:
        app.config.from_object(config_class)

    app.jinja_loader = PrefixLoader({
        "app": PackageLoader("icenet_app"),
        "bas_style_kit": PackageLoader('bas_style_kit_jinja_templates'),
    })
    app.config['BSK_TEMPLATES'] = BskTemplates()
    app.config['BSK_TEMPLATES'].bsk_site_nav_brand_text = 'IceNet'
    app.config['BSK_TEMPLATES'].bsk_site_development_phase = 'alpha'
    app.config['BSK_TEMPLATES'].bsk_site_feedback_href = '/feedback'
    app.config['BSK_TEMPLATES'].bsk_site_footer_policies_cookies_href = '/legal/cookies'
    app.config['BSK_TEMPLATES'].bsk_site_footer_policies_copyright_href = '/legal/copyright'
    app.config['BSK_TEMPLATES'].bsk_site_footer_policies_privacy_href = '/legal/privacy'
    app.config['BSK_TEMPLATES'].site_description = 'IceNet Dashboard and API services'
    app.config['BSK_TEMPLATES'].site_styles.append({'href': '/static/css/main.css'})
    app.config['BSK_TEMPLATES'].site_title = 'IceNet Dashboard'

    return app


app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("app/errors/404.j2"), 404


@app.route('/')
def index():
    service = urlparse(request.base_url).netloc.split(":")[0].split(".")[0]
    logging.info("{} has service {}".format(request.base_url, service))

    if service == "api":
        location = "{}api/ui".format(request.base_url)
        logging.info("Redirecting to the API at {}".format(location))
        return redirect(location, 301)
    return render_template("app/index.j2")

