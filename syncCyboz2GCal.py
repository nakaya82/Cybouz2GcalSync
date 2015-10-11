#! /usr/bin/env python
# -*- coding: utf-8 -*-

import getCyCal
import setGCal
import configparser
import sys

import httplib2
from apiclient import discovery


if __name__ == "__main__":
    status = False

    conf = configparser.ConfigParser()
    conf.read('cyschesync.cfg')

    account = conf['cybouz']['account']
    password = conf['cybouz']['password']
    url = conf['cybouz']['url']
    ical_file = conf['cybouz']['ical_file']

    with getCyCal.getCybouzSchedule(account, password, url) as request:
        status = getCyCal.createIcsFile(request, ical_file)

    if not status:
        print("Cybouzよりスケジュールの取り出しに失敗しました")
        sys.exit()
    else:
        print("Cybouzよりスケジュールの取り出しに成功しました")

    scopes = conf['google_api']['scopes']
    scert_file = conf['google_api']['client_secert_file']
    appname = conf['google_api']['application_name']

    credentials = setGCal.get_credentials(scopes, scert_file, appname)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # 該当colorのEventを削除
    color_id = conf['google_api']['colorId']
    ical_file = conf['cybouz']['ical_file']

    setGCal.deleteEvents2Gcal(service, color_id)
    events = setGCal.readIcalFile(ical_file)
    status = setGCal.insertEventList2Gcal(service, events, color_id)
    if status:
        print("Googleカレンダーに予定をインポートしました")
    else:
        print("Googleカレンダーに予定をインポート出来ませんでした")
