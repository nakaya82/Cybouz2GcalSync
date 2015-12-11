# Cybouz2GcalSync #
====

## Overview ##
Cybouzカレンダーの2ヶ月分の月次予定をGoogleカレンダーへインポートするプログラム

## Description ##
以下の処理を行っています。

1. cybouzより2ヶ月分の月次予定情報（icalファイル）を取得
2. googleカレンダーの予定を取得
3. 該当カラー（設定ファイルにて指定。デフォルト9）の予定を削除
4. cybouz予定情報をひとつずつimport

## Usage
crontabに以下を設定するなどし、定期的に同期させます。
```
0,30 * * * * cd ~/cybouz2gcalsync; python3 ~/cybouz2gcalsync/syncCyboz2GCal.py 
```

## Install ##
    $ cd ~
    $ git clone https://github.com/nakaya82/Cybouz2GcalSync.git
    $ cd cybouz2gcalsync
    $ pip install -r requirements.txt
    $ vi cyschesync.cfg
        サイボウズのid/pwを設定してください
        account: <cybouz account>
        password: <cybouz password>
        url: <cybouz url>
    $ python3 syncCyboz2GCal.py --noauth_local_webserver
Google認証システムにて、同期したいアカウントでGoogle認証ログインして下さい。

初回ログイン時、コマンドから返されるURLにアクセスし、Google認証ログインする必要があります。

後は、上記Usage通り、crontab -eで設定して下さい。
