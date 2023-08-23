#!/usr/bin/env bash

if [ ! -d venv ]; then
	echo "You're running without a virtual environment, this probably isn't set up right"
	exit 1
fi

export FLASK_APP="icenet_app.app"
export FLASK_DEBUG=True
export FLASK_ENVIRONMENT=development
export ICENET_DATA_LOCATION=${ICENET_DATA_PATH:-./data}

flask run --debug
