#!/usr/bin/env python3

import argparse
import calendar
import datetime

#import signal

import locale
import logging
import time

import os
import os.path
import sys

log = logging.getLogger(__name__)

# Our output format
def user_datetime(when):
    """Print time for the user"""
    return when.ctime()

class CTT:
    def __init__(self, project):
        self.project = project
        self.tracked_time = False

        self._init_home()


    def _init_home(self):
        # Create output directory
        home = os.environ['HOME']
        self.ctt_dir = os.path.join(home, ".ctt")
        self.project_dir = os.path.join(self.ctt_dir, self.project)


    # Track time and return information from tracking
    def track_time(self):
        self.start = datetime.datetime.now()

        try:
            # Dummy read data to wait for keyboard irq
            input()
        except KeyboardInterrupt:
            pass

        self.stop = datetime.datetime.now()

        self.tracked_time = True

    def write_time(self):
        if not self.tracked_time:
            return

        start_seconds =  self.start.strftime("%s")
        stop_seconds =  self.stop.strftime("%s")
        time_dir = os.path.join(self.project_dir, start_seconds)
        os.makedirs(time_dir, mode=0o700, exist_ok=True)

        filename = os.path.join(time_dir, "end")

        with open(filename, "w") as fd:
            fd.write("%s\n" % stop_seconds)

    def duration(self):
        if self.tracked_time:
            delta = self.stop - self.start
        else:
            delta = 0

        return delta


# Setup locale for calendar printing
# Setup locale to get Timezone information?
#print(locale.getlocale())

# Record project
# Record tags

parser = argparse.ArgumentParser()
parser.add_argument("project", help="Project to track time for", nargs=1)
parser.add_argument("-t", "--track", help="Track time (until Ctrl-C is pressed)",
    action="store_true")

args = parser.parse_args(sys.argv[1:])
print(args)

ctt = CTT(args.project[0])

ctt.track_time()
ctt.write_time()
print(ctt.duration())

sys.exit(0)

# Setup signal handler

# Start tracking
# Save stuff to our home directory

# Create datetime from userinput
# Wed Aug  1 23:35:53 2012
