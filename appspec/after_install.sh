#!/bin/bash
ENVDIR="/var/app/venv/"
if [ ! -d "$ENVDIR" ]; then
  mkdir /var/app
  mkdir /var/app/venv
  python3 -m venv /var/app/venv
fi
. /var/app/venv/bin/activate
pip install -r /var/app/current/requirements.txt --user
