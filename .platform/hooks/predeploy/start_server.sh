source /var/app/venv/staging-LQM1lest/bin/activate
cd /var/app/current
gunicorn django_project.wsgi
mkdir /home/ec2-user/helloworld