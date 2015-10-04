#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.parse
import urllib.request
import configparser
from urllib.error import URLError


def getCybouzSchedule():
    conf = configparser.ConfigParser()
    conf.read('chschesync.cfg')
    account = conf['cybouz']['account']
    password = conf['cybouz']['password']
    url = conf['cybouz']['url']

    form = {'_account': account,
            '_password': password,
            '_system': '1'}
    data = urllib.parse.urlencode(form).encode('utf-8')

    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/html,application/xhtml+xml,application/xml;\
               q=0.9,*/*;q=0.8",
               "Connection": "keep-alive",
               "Host": "gw.garage.co.jp",
               "User-Agent":
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit\
               /537.36 (KHTML, like Gecko)\ Chrome/45.0.2454.99 Safari/537.36"}

    request = urllib.request.Request(url, data, headers)
    try:
        return urllib.request.urlopen(request)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)


def createIcsFile(response):
    with open('schedule.ics', 'w', encoding='utf-8') as ofs:
        ofs.write(response.readline().decode('utf-8'))
        ofs.close()


if __name__ == "__main__":
    with getCybouzSchedule() as request:
        createIcsFile(request)
