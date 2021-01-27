#!/bin/bash
source "/etc/profile.d/custom-envs.sh"
. /home/ec2-user/venv/bin/activate
cd ~
if [ $PP_ENVIRONMENT != "Production" ]
then
  dbhost=$(aws secretsmanager get-secret-value --secret-id "$DB_PASS_SECRET_NAME" | python3 -c "import sys, json; print(json.loads(json.load(sys.stdin)['SecretString'])['host'])")
  dbname=$(aws secretsmanager get-secret-value --secret-id "$DB_PASS_SECRET_NAME" | python3 -c "import sys, json; print(json.loads(json.load(sys.stdin)['SecretString'])['dbname'])")
  dbuser=$(aws secretsmanager get-secret-value --secret-id "$DB_PASS_SECRET_NAME" | python3 -c "import sys, json; print(json.loads(json.load(sys.stdin)['SecretString'])['username'])")
  dbpass=$(aws secretsmanager get-secret-value --secret-id "$DB_PASS_SECRET_NAME" | python3 -c "import sys, json; print(json.loads(json.load(sys.stdin)['SecretString'])['password'])")
  aws s3 cp s3://elasticbeanstalk-us-west-2-054058811484/DbStarters/db.sql ./db.sql
  mysql -u "$dbuser" -p"$dbpass" -h "$dbhost" -e "DROP DATABASE $dbname;"
  mysql -u "$dbuser" -p"$dbpass" -h "$dbhost" -e "CREATE DATABASE $dbname;"
  mysql -u "$dbuser" -p"$dbpass" -h "$dbhost" "$dbname" < db.sql
  rm db.sql
fi
cd /var/app/current
python3 manage.py migrate