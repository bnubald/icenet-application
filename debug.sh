#!/usr/bin/env bash

if [ ! -d venv ]; then
	echo "You're running without a virtual environment, this probably isn't set up right"
	exit 1
fi

./venv/bin/python icenet_application/app.py
