#!/usr/bin/env bash

if [ ! -d venv ]; then
	echo "You're running without a virtual environment, this probably isn't set up right"
	exit 1
fi

export FLASK_APP="icenet_app.app"
export FLASK_ENVIRONMENT=development
export ICENET_APP_ENV=development
export ICENET_AUTH_LIST=`pwd`/auth_list.json
export ICENET_DATA_LOCATION=${ICENET_DATA_LOCATION:-/data}

flask run --debug
