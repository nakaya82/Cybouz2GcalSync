#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import getCyCal
import setGCal
import configparser
import sys

import httplib2
from apiclient import discovery
from datetime import date as dt


def verify(status):
    if not status:
        print("Cybouzよりスケジュールの取り出しに失敗しました")
        sys.exit()
    else:
        print("Cybouzよりスケジュールの取り出しに成功しました")


if __name__ == "__main__":
    status = False

    conf = configparser.ConfigParser()
    conf.read('cyschesync.cfg')

    account = conf['cybouz']['account']
    password = conf['cybouz']['password']
    url = conf['cybouz']['url']
    today = dt.today()
    ical = conf['cybouz']['ical_file']
    thisMical = ical + "_" + today.strftime('%Y%m')
    nextMon = dt(today.year + (today.month == 12), today.month % 12 + 1, 1)
    nextMical = ical + "_" + nextMon.strftime('%Y%m')

    # 今月のデータをCybouzからエクスポート
    with getCyCal.getCybouzSchedule(
            account, password, url, today.strftime('%Y-%m-01')) as request:
        status = getCyCal.createIcsFile(request, thisMical)
        verify(status)
    # 来月のデータをCybouzからエクスポート
    with getCyCal.getCybouzSchedule(
            account, password, url, nextMon.strftime('%Y-%m-01')) as request:
        status = getCyCal.createIcsFile(request, nextMical)
        verify(status)

    scopes = conf['google_api']['scopes']
    scert_file = conf['google_api']['client_secert_file']
    appname = conf['google_api']['application_name']

    credentials = setGCal.get_credentials(scopes, scert_file, appname)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # 該当colorのEventを削除
    color_id = conf['google_api']['colorId']

    setGCal.deleteEvents2Gcal(service, color_id)
    events = []
    # 今月のデータをGoogleCalendarにインポート
    events = setGCal.readIcalFile(events, thisMical, today, nextMon)
    # 来月月のデータをGoogleCalendarにインポート
    events = setGCal.readIcalFile(
        events, nextMical, nextMon, dt(
            nextMon.year + (nextMon.month == 12), nextMon.month % 12 + 1, 1))
    status = setGCal.insertEventList2Gcal(service, events, color_id)
    if status:
        print("Googleカレンダーに予定をインポートしました")
    else:
        print("Googleカレンダーに予定をインポート出来ませんでした")
