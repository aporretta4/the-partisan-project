yum -y update

# Installing software.

# Mysql
mysqltest=`yum list installed bind`
if [ "$mysqltest"="Error: No matching Packages to list" ]; then
  yum install -y mysql
fi

#Supervisor
easy_install supervisor
if [ ! -d "/etc/supervisor" ]; then
  mkdir /etc/supervisor
fi
cp /var/app/staging/.platform/hooks/prebuild/copy_files/supervisor.conf /etc/supervisor/supervisor.conf
cp /var/app/staging/.platform/hooks/prebuild/copy_files/supervisord /usr/bin/supervisord

# Pip dependencies for app.
/usr/local/bin/pip install -r /var/app/staging/requirements.txt