# encoding: utf-8
from __future__ import print_function
from fabric.api import execute, local, task
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
    import datetime
    now = datetime.datetime.now()
    conn = _connect()
    conn.autocommit(False)
    for i in range(10000):
        sql = "INSERT INTO articles (blog_id, title, body, published, published_at) VALUES "
        params = []
        for j in range(10):
            sql += "(%s, %s, %s, %s, %s),"
            content = _generate_article_content(i)
            params.extend([i+1, content[0], content[1], 1, now.strftime("%Y-%m-%d %H:%M:%S")])
        sql = sql[:-1]
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
        if i % 100 == 0:
            conn.commit()
    conn.commit()
    conn.close()


@task
def generate_all():
    execute(generate_blogs)
    execute(generate_articles)


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

article_contents = [
    [
        "Heroku Schedulerやcronが正常に稼働しているかをチェックするDead Man's Snitchが便利",
        """
これは[Heroku Advent Calendar 2015](http://qiita.com/advent-calendar/2015/heroku) 21日の記事です。今回はHeroku Schedulerを監視する[Dead Man's Snitch](https://deadmanssnitch.com/)というものを紹介します。

### Heroku Schedulerってなに？

Heroku上で特定のスクリプトやコマンドを動かすcronみたいなもの。「みたいなもの」というのは、cronと違って「何時何分に実行する」というような厳密な時間指定ができず、10分、1時間、1日単位でしか指定ができません。イメージとしては以下のような感じ。

![Heroku Scheduler setting](https://github.com/oinume/dmm-eikaiwa-tsc/raw/master/doc/heroku_scheduler.png?raw=true "Heroku Scheduler setting")

ただ、このような要件でも十分であれば、無料のDynoでも利用できるのがメリットだと思います。


### Dead Man's Snitchでコマンドが正常に稼働しているかチェックする
Heroku Schedulerで動かしているコマンドが正常に稼働しているかをチェックすることができないか？と思って調べていたらこのDead Man's Snitchに行き着きました。原理としては

1. Heroku Schedulerに`your_command.sh && curl https://nosnch.in/<hash>`のようにコマンドを登録しておき、your_command.shが成功した時にcurlで成功したということをDead Man's Snitchに送信する(チェックイン)
1. Dead Man's Snitch側では、1時間の間隔(*1)でちゃんとコマンドが成功しチェックインされたかどうかをチェック
1. もし1時間以上チェックインしていなければ、指定したメールアドレスにアラートメールが送信される

という流れです。チェックインをチェックする間隔は1日, 1週間などの間隔が設定可能で、有料プランだと15分、30分の間隔もできるようです。

ちなみにチェックインされていない場合に送られてくるアラートメールはこんな感じ。

```
Hi <app>,

FYI "<app>" doesn't seem to be working.

Last healthy check-in: about 8 hours ago (16 Dec 16:13 UTC)

You might want to check it out:

https://deadmanssnitch.com/snitches/<hash>

Would you like to pause your snitch?

https://deadmanssnitch.com/snitches/<hash>/pause

Kind regards,

Dead Man's Snitch
```

なおこのDead Man's Snitchは特定のURLにGETでアクセスするだけのシンプルな仕組みなので、Heroku Schedulerだけではなくcronでも使えます。もちろんcurlからではなくプログラムのコードからでも呼び出せます。


### まとめ
Heroku Schedulerやcronの死活監視に使えるDead Man's Snitchというサービスを紹介しました。データーベースのデータをバックアップするような重要なスクリプトにDead Man's Snitchによる死活監視を入れておくとスクリプトが動作していないことにすぐ気付けるのでオススメです。
        """
    ],
    [
        "MySQLでbulk insert + on duplicate key updateしたい",
        """
MySQLで`INSERT INTO hoge VALUES (...), (...), (...)`のbulk insertでon duplicate key update(すでにレコードがあったらUPDATEで上書きする)って併用できるのかな？っていうのが気になったので調べてみたらできるみたい。[VALUES関数](https://dev.mysql.com/doc/refman/5.6/ja/miscellaneous-functions.html#function_values)というその目的のためだけに存在するような関数を使う。

こんな感じでテーブル作って

```sql
CREATE TABLE users (
    name VARCHAR(255) NOT NULL,
    age TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (name)
) ENGINE=InnoDB;
```

データをINSERTして

```sql
INSERT INTO users VALUES
  ('akuwano', 25), ('oinume', 24), ('oranie', 23);

SELECT * FROM users;
+---------+-----+
| name    | age |
+---------+-----+
| akuwano |  25 |
| oinume  |  24 |
| oranie  |  23 |
+---------+-----+
```

`INSERT ... ON DUPLICATE KEY UPDATE`で重複したレコードがあった場合に全てアップデートされるかな？

```sql
INSERT INTO users VALUES
  ('akuwano', 15), ('oinume', 14), ('oranie', 13)
  ON DUPLICATE KEY UPDATE age = VALUES(age);

mysql> SELECT * FROM users;
+---------+-----+
| name    | age |
+---------+-----+
| akuwano |  15 |
| oinume  |  14 |
| oranie  |  13 |
+---------+-----+
```

<span style="font-size: xx-large">された！！</span>

[asin:4873116384:detail]
        """
    ],
    [
        "ターミナルとキーボードだけでプルリクエストを送る",
        """
これは[Sending pull-request only with terminal and keyboard](/entry/sending-pull-request-only-with-terminal-and-keyboard)の日本語の記事です。


### 必要なもの

* Mac
* Terminal
* hub command (`brew install hub`でインストールしておく)


### How to send pull-request

ブランチを作る
```
$ git checkout -b new-cool-feature
```

ソースを編集する
```
$ git commit -a
```

わざとgit pushしてエラーにして、正しいコマンドをpbcopyでクリップボードにコピー
```
$ git push 2>&1 | grep git | pbcopy
```

Cmd+Vでペーストしてpush
```
$ git push --set-upstream origin new-cool-feature

Counting objects: 3, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 324 bytes | 0 bytes/s, done.
Total 3 (delta 2), reused 0 (delta 0)
To git@github.com:example/example-project.git
 * [new branch]      new-cool-feature -> new-cool-feature
Branch new-cool-feature set up to track remote branch new-cool-feature from origin.
```

`hub`コマンドでプルリクエストを作成
```
$ hub pull-request
https://github.com/example/example-project/pull/1
```
        """,
    ]
]

def _generate_article_content(id):
    return article_contents[0]
