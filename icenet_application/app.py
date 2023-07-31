import os

from flask import Flask, render_template, request
import connexion
import logging
import os

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("connexion").setLevel(logging.INFO)

app = connexion.App(__name__, specification_dir="../")
app.add_api("swagger.yml")


@app.route('/')
def index():
   return render_template('index.html')


if __name__ == '__main__':
   app.run(host="127.0.0.1", debug=True)
