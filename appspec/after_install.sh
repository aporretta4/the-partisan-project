#!/bin/bash
ENVDIR="/home/ec2-user/venv/"
pkill gunicorn
if [ ! -d "$ENVDIR" ]; then
  python3 -m venv /home/ec2-user/venv
fi
chown -R ec2-user /home/ec2-user/venv
chmod 775 /home/ec2-user/venv/bin/activate
. /home/ec2-user/venv/bin/activate
pip3 install -r /var/app/current/requirements.txt
python3 manage.py migrate
rm -R django_project/static/*
python3 manage.py collectstatic --noinput
aws s3 sync "partisan/static/" "s3://$STATIC_FILE_BUCKET_NAME"
/home/ec2-user/venv/bin/gunicorn --bind 127.0.0.1:8000 django_project.wsgi --daemon
