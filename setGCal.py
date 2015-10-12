#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os

import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import icalendar

import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()


def get_credentials(scopes, secert_file, appname):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(secert_file, appname)
        flow.user_agent = appname
        credentials = tools.run_flow(flow, store, flags)
    return credentials


# read Event from ics file
def readIcalFile(ical_file):
    events = []

    try:
        with open(ical_file, "r") as fh:
            ical_str = fh.read()
            fh.close()
    except IOError as e:
        print("iCal file open error")
        return

    cal = icalendar.Calendar.from_ical(ical_str)

    for e in cal.walk():
        if e.name == 'VEVENT':
            start_str = e.decoded("dtstart").strftime('%Y-%m-%d %H:%M:%S')
            start_dt = datetime.datetime.strptime(
                start_str, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.utcnow()
            if (now > start_dt):
                continue
            dict_schedule = {
                "title": e.decoded("summary").decode('utf-8') if
                e.get("summary") else "",
                "place": e.decoded("location").decode('utf-8') if
                e.get("location") else "",
                "desc": e.decoded("description").decode('utf-8') if
                e.get("description") else "",
                "rrule": e.decoded("rrule") if e.get("rrule") else "",
                "start": e.decoded("dtstart"),
                "end": e.decoded("dtend"),
            }
            events.append(dict_schedule)
    return events


def insertEventList2Gcal(service, events, color_id):
    status = False
    # Eventリストが空の場合は何もしない
    if service is None or events is None or len(events) <= 0:
        print('insertするEventはありません')
        return

    for event in events:

        body = {
            'summary': event['title'],
            'location': event['place'],
            'description': event['desc'],
            'start': {
                'dateTime': event['start'].strftime('%Y-%m-%dT%H:%M:%S+09:00'),
                'timeZone': 'Asia/Tokyo',
            },
            'end': {
                'dateTime': event['end'].strftime('%Y-%m-%dT%H:%M:%S+09:00'),
                'timeZone': 'Asia/Tokyo',
            },
            "colorId": color_id,
        }
        if event['rrule']:
            body['recurrence'] = event['rrule'].to_ical().decode('utf-8')

        # print(body)

        event = service.events().insert(
            calendarId='primary', body=body).execute()
        if event is not None:
            status = True
        # print('Event created: %s' % (event.get('htmlLink')))
    return status


def deleteEvents2Gcal(service, color_id):
    if service is None:
        return
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z'indicates UTC time
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now).execute()
    all_events = eventsResult.get('items', [])
    events = []
    for event in all_events:
        if 'colorId' in event and color_id == event['colorId']:
            events.append(event)
    if events is None or len(events) <= 0:
        print('消したいeventはありません')
        return
    else:
        print('eventを消去します')
        # print(events)
    for event in events:
        service.events().delete(
            calendarId='primary', eventId=event['id']).execute()
