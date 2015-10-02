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
$ git clone git@gitlab.boi.tokyo:kpi/s3log-gripper.git
$ python setup.py install
```

## How to Use

取得できるログの一覧を表示

```
$ gripper -l
```
