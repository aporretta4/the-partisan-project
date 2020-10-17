#!/bin/bash
ENVDIR="/home/ec2-user/venv/"
pkill gunicorn
if [ ! -d "$ENVDIR" ]; then
  python3 -m venv /home/ec2-user/venv
  chown -R ec2-user /home/ec2-user/venv
fi
. /home/ec2-user/venv/bin/activate
pip3 install -r /var/app/current/requirements.txt
cd /var/app/current
python3 manage.py migrate
/home/ec2-user/venv/bin/gunicorn --bind 127.0.0.1:8000 django_project.wsgi --daemon
