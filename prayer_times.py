#!/usr/local/bin/python

import re
import sys
import logging
import argparse
from urllib2 import urlopen
from datetime import datetime as dt
from collections import OrderedDict


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('PRAYERTIMES ')

COVERED_CITIES = [
    'athlone',
    'carlow',
    'cavan',
    'cork',
    'drogheda',
    'dublin',
    'dundalk',
    'ennis',
    'galway',
    'letterkenny',
    'limerick',
    'kilkenny',
    'sligo',
    'waterford',
    'wexford'
]
PTIME_MATCHER = re.compile(
    "(?P<fajr>\d\d:\d\d).*"
    "(?P<shurooq>\d\d:\d\d).*"
    "(?P<dhuhr>\d\d:\d\d).*"
    "(?P<asr>\d\d:\d\d).*"
    "(?P<maghrib>\d\d:\d\d).*"
    "(?P<isha>\d\d:\d\d)"
)
ICC_URL = 'http://islaminireland.com/timetable/{city}'
PRAYERS = ['fajr', 'shurooq', 'dhuhr', 'asr', 'maghrib', 'isha']
COUNTDOWN_BANNER = 'next prayer ({prayer}) due in {time} minutes'


def get_options():
    parser = argparse.ArgumentParser(
        add_help=True,
        usage='./prayer_times.py <city> <mode>'
    )

    parser.add_argument(
        '-c',
        default='dublin',
        choices=COVERED_CITIES,
        dest='desired_city',
        help='Desired City'
    )
    parser.add_argument(
        '-m',
        dest='execution_mode',
        default='short',
        choices=['short', 'long'],
        help='Execution mode'
    )

    options = parser.parse_args()

    return options


def get_prayer_times(city):
    crawler = urlopen(ICC_URL.format(city=city)).read()
    start_tag = 'Prayer Timetable for'
    end_tag = '<!--//donate-->'
    raw_data = crawler[crawler.find(start_tag):crawler.find(end_tag)]
    prayer_times = re.search(PTIME_MATCHER, raw_data).groups()

    time_table = OrderedDict(zip(PRAYERS, prayer_times))

    return time_table


def get_next_prayer_due(time_table):
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
    options = get_options()
    city, mode = options.desired_city, options.execution_mode
    time_table = get_prayer_times(city)
    next_prayer, due_time = get_next_prayer_due(time_table)

    print (COUNTDOWN_BANNER.format(prayer=next_prayer, time=due_time))
    if mode == 'long':
        for prayer, time in time_table.items():
            print ('{}\t:{}'.format(prayer, time))


if __name__ == '__main__':
    main()
