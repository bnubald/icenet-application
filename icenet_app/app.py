import os

from flask import Flask, render_template, request
import connexion
import logging
import os

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("connexion").setLevel(logging.INFO)


def create_app(config_class=None):
    connexion_app = connexion.App(__name__,
                                  specification_dir="../")
    connexion_app.add_api("swagger.yml")
    application = connexion_app.app

    if config_class is not None:
        application.config.from_object(config_class)

    return application


app = create_app()


@app.route('/')
def index():
   return render_template('index.html')

