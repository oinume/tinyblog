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
def generate_blogs():
    sql = "INSERT INTO blogs (name) VALUES "
    names = [
        "doublemarket",
        "strsk",
        "oinume",
        "oranie",
        "akuwano",
        "hiroakis",
        "marqs",
        "mikeda",
        "namikawa",
        "kakerukaeru",
    ]
    params = []
    for name in names:
        for i in range(0, 1000):
            sql += "(%s),"
            params.append("{}-{:04d}".format(name, i+1))
    sql = sql[:-1]
    conn = _connect()
    with conn.cursor() as cursor:
        cursor.execute(sql, params)
    conn.close()


@task
def generate_articles():
    pass


def _connect(
    host="192.168.9.10", port=3306, db="tinyblog",
    user="tinyblog", password="tinyblog"
):
    return pymysql.connect(
        host=host,
        port=port,
        db=db,
        user=user,
        password=password,
        charset="utf8mb4",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor)
