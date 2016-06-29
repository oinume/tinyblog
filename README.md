# tinyblog

# 必要なもの

以下が必要なソフトウェアになるので、適宜インストールして下さい。

- [Vagrant 1.7以上](https://www.vagrantup.com/)
- [VirtualBox 5.0以上](https://www.virtualbox.org/)
- sshコマンド

### Windowsの場合

Windowsの場合は、デフォルトでsshコマンドがインストールされていないので、[Windows版のGit](https://git-scm.com/download/win)をインストールして下さい。これをインストールすると`Git Bash`というプログラムがあわせてインストールされるので、これを起動してこのREADME.mdがあるディレクトリに移動して下さい。


# セットアップ

```
> vagrant up
```

を実行すると、仮想マシンのイメージをダウンロードして、ゲストマシン上に以下のソフトウェアをインストールします。

- MySQL (mysql, mysqldumpslowコマンドなど)
- perconal-toolkit

もし途中でエラーになった場合は

```
> vagrant up
> vagrant provision
```

を実行してみてください。

Windowsの場合、Intel VT-xがBIOSの設定で無効になっていると`vagrant up`で`Warning: Connection timeout. Retrying...`というエラーが出て先に進まないことがあります。[こちら](http://futurismo.biz/archives/1647)を参考にしてBIOSの設定を変更してみてください。

ゲストマシンにsshでログインするには以下のコマンドを実行して下さい。

```
> vagrant ssh
```

なお、仮想マシン上の`/vagrant`ディレクトリは、ホストマシンのこのREADME.mdがあるディレクトリがマウントされています。


# テーブルを作成する

ゲストマシンにsshログインして(`vagrant ssh`)、以下のコマンドを実行して下さい。

```
$ cd /vagrant
$ fab task.db.migrate:version=20160504000000
```

```
$ mysql -uroot -proot tinyblog
```

でMySQLに接続できるので、`show tables`コマンドを実行すると第3章、第4章で使用しているテーブルが作成されているのが確認できます。

### 必要なデータを投入する

テーブルを作成しただけでは、まだ各テーブルにレコードがないため、EXPLAINのコマンドを実行しても本稿で説明したような結果にはならないので、以下のコマンドを実行してデータを投入します。

```
$ cd /vagrant
$ fab task.db.generate_all
```

# データベースに接続したい

ゲストマシンで以下のコマンドを実行して下さい。

```
$ mysql -uroot -proot tinyblog
```

# データベースをリセットしたい

以下のコマンドを実行すると、tinyblogデーターベースを再構築します。

```
$ cd /vagrant
$ fab task.db.reset
```
