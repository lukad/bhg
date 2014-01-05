#!/usr/bin/env python

import argparse
from jinja2 import Template
from collections import namedtuple
import datetime as dt
import random

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", default="Foo", help="Your first name")
parser.add_argument("-l", "--last-name", default="Bar", help="Your last name")
parser.add_argument("-b", "--begin", required=True, help="From wich date to begin (YYYY-MM-DD)")
parser.add_argument("-e", "--end", required=True, help="Stop at this date (YYYY-MM-DD)")
parser.add_argument("-s", "--start-with", default=1, help="Start numbering with this number")
parser.add_argument("-w", "--work-hours", default=8.0, help="How many hours you work per day")

args = parser.parse_args()

Activity = namedtuple("Activity", "name min_duration max_duration weight")

def parse(line):
    if line.startswith("#"):
        return None
    items = line.rstrip().split(";")
    if len(items) < 3:
        return None
    return Activity(items[0], float(items[1]), float(items[2]), int(items[3]))

activities = []

with open("example-input", "r") as f:
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
    return select_weighted([a for a in activities if a.min_duration <= hours_to_fill and a not in already_done])

begin = dt.datetime.strptime(args.begin, "%Y-%m-%d")
end = dt.datetime.strptime(args.end, "%Y-%m-%d")


def main():
   print(select_activity(activities, args.work_hours, []))

if __name__ == '__main__':
    main()
    

#for i in range((end - begin).days + 1):
#    day = (begin + dt.timedelta(days=i)).date()
#    if day.weekday() in [5,6]:
#        continue
#    print(day)
        

# template_string = ""
# with open("template.html", "r") as f:
#     template_string = f.read()



# template = Template(template_string)
# print(template.render(days=days, name=args.name, last_name=args.last_name))
