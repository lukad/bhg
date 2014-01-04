#!/usr/bin/env python

import argparse
from jinja2 import Template
from collections import namedtuple

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", default="Foo", help="Your first name")
parser.add_argument("-l", "--last-name", default="Bar", help="Your last name")

args = parser.parse_args()

Activity = namedtuple("Activity", "name duration weight")

def parse_line(line):
    if line.startswith("#"):
        return None
    items = line.rstrip().split(";")
    if len(items) < 3:
        return None
    return Activity(items[0], float(items[1]), int(items[2]))

benis = ""
with open("example-input", "r") as f:
    for line in f:
        print(parse_line(line))

# template_string = ""
# with open("template.html", "r") as f:
#     template_string = f.read()



# template = Template(template_string)
# print(template.render(days=days, name=args.name, last_name=args.last_name))
