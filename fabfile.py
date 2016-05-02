# encoding: utf-8
from __future__ import print_function
from fabric.api import env, lcd, local, task

@task
def migrate():
    pass


@task
def reset_db():
    local("""vagrant ssh -- "mysql -uroot -e \'DROP DATABASE tinyblog\'" """)
    local("""vagrant ssh -- "mysql -uroot -e \'CREATE DATABASE tinyblog DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci\'" """)
