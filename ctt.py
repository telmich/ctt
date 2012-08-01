#!/usr/bin/env python3

import argparse
import calendar
import datetime

import signal

import locale
import time

import os
import os.path
import sys

#def user_datetime(when):
#    """Print time for the user"""
#    return when.ctime()


# Setup locale for calendar printing
# Setup locale to get Timezone information?
print(locale.getlocale())

# Record project
# Record tags

parser = argparse.ArgumentParser()
parser.add_argument("project_name", nargs=1)

args = parser.parse_args(sys.argv[1:])


sys.exit(0)

# Setup signal handler

# Start tracking
start = datetime.datetime.now()
print("Starting at %s" % (start.ctime()))

time.sleep(2)

# Stop tracking
stop = datetime.datetime.now()
print("Stopped at %s" % (stop.ctime()))

delta = stop - start
print("%s, %s, seconds=%s, %s" % (type(delta), delta, delta.total_seconds(), start.strftime("%s")))

# Save stuff to our home directory

# Prepare home directory
home = os.environ['HOME']
ctt_home = home + os.path.join(home, ".ctt")
os.makedirs(ctt_home, mode=0o700, exist_ok=True)

# Create datetime from userinput
# Wed Aug  1 23:35:53 2012
