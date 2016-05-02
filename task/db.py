# encoding: utf-8
from __future__ import print_function
from fabric.api import abort, env, lcd, local, task


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
