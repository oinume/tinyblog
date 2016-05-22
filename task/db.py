# encoding: utf-8
from __future__ import print_function
from fabric.api import execute, local, task
import datetime
import pymysql
import time
import yaml

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
    sql = "INSERT INTO blogs (name) VALUES "
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
    conn = _connect()
    conn.autocommit(False)
    data = []
    with open('task/articles_data.yml', 'r') as f:
        data = yaml.load(f)

    for i in range(10000):
        sql = "INSERT INTO articles (blog_id, title, body, published, published_at) VALUES "
        params = []
        #now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for j in range(20):
            d = data[j % 10]
            sql += "(%s, %s, %s, %s, %s),"
            params.extend([i+1, u"{} - {} - {}".format(d['title'], i, j), d['body'], d['published'], d['published_at']])
        sql = sql[:-1]
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
        if i % 100 == 0:
            conn.commit()
    conn.commit()

    # Add more 2000 records to blog_id=1
    sql = "INSERT INTO articles (blog_id, title, body, published, published_at) VALUES "
    params = []
    #now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i in range(2000):
        d = data[i % 10]
        sql += "(%s, %s, %s, %s, %s),"
        params.extend([1, u"{} - {}".format(d['title'], i), d['body'], d['published'], d['published_at']])
    sql = sql[:-1]
    with conn.cursor() as cursor:
        cursor.execute(sql, params)
    conn.commit()
    conn.close()


@task
def generate_all():
    execute(generate_blogs)
    execute(generate_articles)


@task
def nplus1_sample1():
    conn = _connect()
    latest_articles = []
    with conn.cursor() as cursor:
        cursor.execute("""
SELECT id, blog_id, title FROM articles
WHERE published = 1
ORDER BY published_at DESC LIMIT 10
        """)
        for row in cursor.fetchall():
            cursor.execute("SELECT name FROM blogs WHERE id = %s", row["blog_id"])
            blog = cursor.fetchone()
            latest_articles.append({
                "id": row["id"],
                "title": row["title"],
                "blog_id": row["blog_id"],
                "blog_name": blog["name"]})
    #import pprint; pprint.pprint(latest_articles)
    conn.close()


@task
def nplus1_sample2():
    conn = _connect()
    latest_articles = []
    with conn.cursor() as cursor:
        cursor.execute("""
SELECT id, blog_id, title FROM articles
WHERE published = 1
ORDER BY published_at DESC LIMIT 10
        """)
        blog_ids = []
        blog_names = {}
        for row in cursor.fetchall():
            latest_articles.append({
                "id": row["id"],
                "title": row["title"],
                "blog_id": row["blog_id"]})
            blog_ids.append(row["blog_id"])

        if not blog_ids:
            return []
        p = ("%s," * len(blog_ids))[:-1]
        cursor.execute("SELECT id, name FROM blogs WHERE id IN (" + p + ")", blog_ids)
        for row in cursor.fetchall():
            blog_names[row["id"]] = row["name"]
        for article in latest_articles:
            article["blog_name"] = blog_names[article["blog_id"]]

    import pprint; pprint.pprint(latest_articles)
    conn.close()


@task
def bulk_insert_true():
    conn = _connect()
    conn.autocommit(True)
    data = []
    with open('task/articles_data.yml', 'r') as f:
        data = yaml.load(f)

    sql = "INSERT INTO articles (blog_id, title, body, published, published_at) VALUES "
    params = []
    for i in range(1000):
        # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        d = data[i % 10]
        sql += "(%s, %s, %s, %s, %s),"
        params.extend([1, u"{} - {}".format(d['title'], i), d['body'], d['published'], d['published_at']])
    sql = sql[:-1]
    elapsed = 0
    with conn.cursor() as cursor:
        #cursor.max_stmt_length = cursor.max_stmt_length * 1024
        start = datetime.datetime.now()
        cursor.execute(sql, params)
        elapsed = (datetime.datetime.now() - start).microseconds
    print("elapsed = {}".format(elapsed))
    conn.close()


@task
def bulk_insert_false():
    conn = _connect()
    conn.autocommit(True)
    data = []
    with open('task/articles_data.yml', 'r') as f:
        data = yaml.load(f)

    elapsed = 0
    sql = "INSERT INTO articles (blog_id, title, body, published, published_at) VALUES (%s, %s, %s, %s, %s)"
    with conn.cursor() as cursor:
        for i in range(1000):
            params = []
            # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            d = data[i % 10]
            params.extend([1, u"{} - {}".format(d['title'], i), d['body'], d['published'], d['published_at']])

            start = datetime.datetime.now()
            cursor.execute(sql, params)
            elapsed += (datetime.datetime.now() - start).microseconds
    print("elapsed = {}".format(elapsed))
    conn.close()


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
