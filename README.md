# s3log-gripper

## About

`s3log-gripper`はAmazonS3からログを取得してCSV形式で吐き出すコマンドラインツールです.

依存性を生まないためには`pyenv`と`virtualenv`, `virtualenvwrapper`の使用を推奨しますが,

使用せずとも問題なく利用できるはずです.

## Environment

推奨環境は以下の通りです.

* CentOS 6.5
* Python 2.7.6

## Set up

```
$ git clone git@github.com:junishitsuka/s3log-gripper.git
$ python setup.py install
$ sudo yum install -y jq
$ aws configure # set key
```

## Option

設定情報は`src/const.py`に記述されているので、自分の環境に合わせて変更してください。

`const.OUT_FILE`は出力対象となるファイル名で、コマンドを使用したディレクトリに作成されます。

既に同じ名前のファイルが存在していると、削除してからコマンドを実行します。

S3のディレクトリ構成は以下のような想定で実装されています。

`BUCKET_DIR/COLLECTION_NAME/yyyy-mm-dd_i.gz`

or 

`BUCKET_DIR/COLLECTION_NAME/yyyy-mm-dd-hh_i.gz`

`COLLECTION_LIST`は使用可能な`COLLECTION_NAME`のリストとなっています。

## How to Use

取得できるログの一覧を表示

```
$ gripper -l
```

期間を指定してログを取得

```
$ gripper -c login -f 2015-04-01 -t 2015-04-03
```

`awscli`の`profile`オプションを指定してログを取得

```
$ gripper -c login -f 2015-04-01 -t 2015-04-03 -p default
```
