#!/bin/bash

prjName="test_aideco"
appName="airport"
targetDir="/var/$prjName"
gitHub="https://github.com"
gitUser="ShmakovVA"

echo "Installing git..."
sudo apt-get install git
echo "Installing nginx..."
sudo apt-get install nginx
echo "Installing python3..."
sudo apt-get install python3
echo "Installing pip3..."
sudo apt-get install python3-pip
echo "Creation working directory $targetDir..."
mkdir "$targetDir"
echo "Cloning project $prjName to $targetDir..."
git clone "$gitHub/$gitUser/$prjName" "$targetDir"
cd "$targetDir"
echo "Installing project requirements..."
pip3 install -r requirements.txt
echo "Installing uwsgi..."
pip3 install uwsgi
echo "Place link for nginx.conf in nginx..."
ln -s "$targetDir/aideco_nginx.conf" "/etc/nginx/sites-enabled/"
echo "Django manage.py commands..."
python3 manage.py collectstatic
python3 manage.py makemigrations $appName
python3 manage.py migrate
python3 manage.py createsuperuser
echo "Nginx start..."
/etc/init.d/nginx restart
echo "Start via uwsgi..."
uwsgi --ini uwsgi.ini
echo "Autostart on boot..."
sed -i "s/sudo uwsgi --ini \/var\/test_aideco\/uwsgi.ini//g" /etc/rc.local
sed -i "s/exit 0/sudo uwsgi --ini \/var\/test_aideco\/uwsgi.ini\nexit 0/g" /etc/rc.local