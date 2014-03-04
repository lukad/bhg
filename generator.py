#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import argparse
from appy.pod.renderer import Renderer
from collections import namedtuple
import datetime as dt
import random

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", required=True, help="Your first name")
parser.add_argument("-l", "--lastname", required=True, help="Your last name")
parser.add_argument("-d", "--division", required=True, help="Your division")
parser.add_argument("-b", "--begin", required=True, help="From wich date to begin (DD-MM-YYYY)")
parser.add_argument("-e", "--end", required=True, help="Stop at this date (DD-MM-YYYY)")
parser.add_argument("-i", "--input", required=True, help="Input file with activities")
parser.add_argument("-s", "--start-with", default=1, help="Start numbering with this number")
parser.add_argument("-w", "--work-hours", default=8.0, help="How many hours you work per day")
parser.add_argument("-t", "--template", required=True, help="Template file")

args = parser.parse_args()

Activity = namedtuple("Activity", "name min_duration max_duration weight filler")

months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

def parse(line):
    if line.startswith("#"):
        return None
    items = line.rstrip().split(";")
    if len(items) < 5:
        return None
    return Activity(
            name = items[0],
            min_duration = float(items[1]),
            max_duration = float(items[2]),
            weight = int(items[3]),
            filler = items[4] == "1")

activities = []

with open(args.input, "r") as f:
    for line in f:
        activity = parse(line)
        if activity is not None:
            activities.append(activity)

def select_weighted(activities):
    total = sum(activity.weight for activity in activities)
    rnd = random.random() * total
    for activity in activities:
        if rnd < activity.weight:
            return activity
        rnd -= activity.weight

def select_activity(activities, hours_to_fill, already_done):
    l = [a for a in activities if a not in already_done and a.min_duration <= hours_to_fill and not a.filler]
    return select_weighted(l)

def select_filler(activities, hours_to_fill, already_done):
    l = [a for a in activities if a not in already_done and a.min_duration <= hours_to_fill and a.filler]
    return random.choice(l)

begin = dt.datetime.strptime(args.begin, "%d.%m.%Y")
end = dt.datetime.strptime(args.end, "%d.%m.%Y")

def save_week(begin, end, month, number, days):
    renderer = Renderer(args.template, {
        'days': days,
        'begin': begin,
        'end': end,
        'month': months[month-1],
        'number': number,
        'name': args.name,
        'lastname': args.lastname,
        'division': args.division
        }, "%s-%s.odt" % (begin, end))
    renderer.run()
        
weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]

def main():
    week = args.start_with
    days = []
    for i in range((end - begin).days + 1):
        day = (begin + dt.timedelta(days=i)).date()
        if day.weekday() in [5,6]:
            continue
        hours_worked = 0
        done = []
        while hours_worked < args.work_hours:
            activity = select_activity(activities, args.work_hours - hours_worked, done)
            if activity is None:
                activity = select_filler(activities, args.work_hours - hours_worked, done)
            done.append(activity)
            hours_worked += activity.min_duration
        days.append({"name": weekdays[day.weekday()], "date": day.strftime("%d.%m.%Y"), "activities": done, "hours_worked": hours_worked})

        if day.weekday() == 4:
            week_begin = day - dt.timedelta(days=4)
            save_week(week_begin, day, week_begin.month, week, days)
            week += 1
            days = []

if __name__ == '__main__':
    main()
