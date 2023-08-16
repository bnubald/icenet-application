import logging
from urllib.parse import urlparse

from bas_style_kit_jinja_templates import BskTemplates
from flask import redirect, render_template, request
from jinja2 import PrefixLoader, PackageLoader

import connexion

logging.getLogger().setLevel(logging.DEBUG)

from icenet_app.plots import default_plot, geoapi_plot


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

    return render_template("app/index.j2",
                           icenet_coverage=geoapi_plot(),
                           icenet_histogram=default_plot(),
                           icenet_map=default_plot(),
                           icenet_sie_change=default_plot(),
                           icenet_uncertainty=default_plot())
