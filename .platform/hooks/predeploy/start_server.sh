command source /var/app/venv/staging-LQM1lest/bin/activate
command cd /var/app/current
command gunicorn django_project.wsgi
command mkdir /home/ec2-user/helloworld