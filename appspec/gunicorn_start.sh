#!/bin/bash
source "/etc/profile.d/custom-envs.sh"
. /home/ec2-user/venv/bin/activate
cd /var/app/current
pkill gunicorn
/home/ec2-user/venv/bin/gunicorn --bind 127.0.0.1:8000 django_project.wsgi --daemon