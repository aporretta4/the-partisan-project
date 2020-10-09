#!/bin/bash
ENVDIR="/home/ec2-user/venv/"
if [ ! -d "$ENVDIR" ]; then
  python3 -m venv /home/ec2-user/venv
fi
. /home/ec2-user/venv/bin/activate
pip install -r /var/app/current/requirements.txt --user
