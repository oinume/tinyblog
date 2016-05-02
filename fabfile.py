# encoding: utf-8
from __future__ import print_function
from fabric.api import abort, env, lcd, local, task
import sys

@task
def migrate_db(version):
    local("""vagrant ssh -- "cd /vagrant && db-migrate --migration={version}" """.format(**locals()))


@task
def reset_db():
    local("""vagrant ssh -- "mysql -uroot -proot -e \'DROP DATABASE tinyblog\'" """)
    local("""vagrant ssh -- "mysql -uroot -proot -e \'CREATE DATABASE tinyblog DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci\'" """)

