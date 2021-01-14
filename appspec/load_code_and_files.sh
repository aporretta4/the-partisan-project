#!/bin/bash
source "/etc/profile.d/custom-envs.sh"
. /home/ec2-user/venv/bin/activate
pkill gunicorn
pip3 install -r /var/app/current/requirements.txt
cd /var/app/current
aws s3 sync "partisan/static/" "s3://$STATIC_FILE_BUCKET_NAME/static"
/home/ec2-user/venv/bin/gunicorn --bind 127.0.0.1:8000 django_project.wsgi --daemon
