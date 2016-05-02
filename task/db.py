# encoding: utf-8
from __future__ import print_function
from fabric.api import abort, env, lcd, local, task
import pymysql

@task
def migrate(version):
    local("""vagrant ssh -- "cd /vagrant && db-migrate --migration={version}" """.format(**locals()))


@task
def reset():
    local("""vagrant ssh -- "mysql -uroot -proot -e \'DROP DATABASE tinyblog\'" """)
    local("""vagrant ssh -- "mysql -uroot -proot -e \'CREATE DATABASE tinyblog DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci\'" """)


@task
def mysqldump():
    local("""vagrant ssh -- "cd /vagrant && mysqldump -uroot -proot --single-transaction --order-by-primary --compress --compact --add-drop-database --default-character-set=utf8mb4 tinyblog > tinyblog.dump.sql" """)


@task
def generate_data():
    conn = pymysql.connect(
        host="192.168.9.10",
        db="tinyblog",
        user="tinyblog",
        password="tinyblog",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1")
        for row in cursor.fetchall():
            print(row)
    conn.close()
