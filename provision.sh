#!/bin/sh

sudo apt update
echo "mysql-server-5.6  mysql-server/root_password password root" | sudo debconf-set-selections
echo "mysql-server-5.6  mysql-server/root_password_again password root" | sudo debconf-set-selections
sudo apt install -y mysql-server-5.6 mysql-client-5.6 libmysqlclient-dev
mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS tinyblog DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;"
mysql -uroot -proot -e "GRANT ALL ON tinyblog.* TO tinyblog@'%' IDENTIFIED BY 'tinyblog';"
mysql -uroot -proot -e "GRANT ALL ON tinyblog.* TO tinyblog@'localhost' IDENTIFIED BY 'tinyblog';"

sudo apt install -y python-pip python-dev
sudo pip install -r requirements.txt
