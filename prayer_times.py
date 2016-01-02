#!/usr/local/bin/python

import re
import sys
from urllib2 import urlopen
from datetime import datetime as dt
from collections import OrderedDict


MATCHER = re.compile(
    "(?P<fajr>\d\d:\d\d).*"
    "(?P<shurooq>\d\d:\d\d).*"
    "(?P<dhuhr>\d\d:\d\d).*"
    "(?P<asr>\d\d:\d\d).*"
    "(?P<maghrib>\d\d:\d\d).*"
    "(?P<isha>\d\d:\d\d)"
)


def get_prayer_times():
    page = urlopen('http://islaminireland.com/timetable/dublin/').read() # replace dublin with your city in Ireland
    start_tag = 'Prayer Timetable for Dublin'
    end_tag = '<!--//donate-->'
    raw_data = page[page.find(start_tag):page.find(end_tag)]
    prayer_times = re.search(MATCHER, raw_data).groups()

    prayers = ['fajr', 'shurooq', 'dhuhr', 'asr', 'maghrib', 'isha']
    time_table = OrderedDict(zip(prayers, prayer_times))

    return time_table


def get_countdown(time_table):
    time_format = '%H:%M'
    current_time = dt.strftime(dt.now(), time_format)

    for prayer, ptime in time_table.items():
        difference = int(
            (dt.strptime(ptime, time_format) - dt.strptime(current_time, time_format)).total_seconds()
        )

        if difference > 0:
            minutes, _ = divmod(difference, 60)
            return (prayer, minutes)


def main():
    time_table = get_prayer_times()
    countdown = get_countdown(time_table)
    countdown_banner = 'next prayer ({}) due in {} minutes'.format(countdown[0], countdown[1])

    print countdown_banner
    if sys.argv[1] == 'long':
        for prayer, time in time_table.items():
            print '{}\t:{}'.format(prayer, time)



if __name__ == '__main__':
    main()
