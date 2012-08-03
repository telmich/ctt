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

VERSION = "0.1"

# Our output format
def user_datetime(when):
    """Print time for the user"""
    return when.ctime()

class Tracker:
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
            # Wait for the exception to pop up - FIXME: find better method

            # Using input, Ctrl-C is displayed as ^C on the screen - ugly
            #input()

            # Sleep 42 years - should be longer than anybody trying to track time
            time.sleep(86400 * 365 * 42)

        except KeyboardInterrupt:
            pass

        self.stop = datetime.datetime.now()

        self.tracked_time = True

    def write_time(self):
        if not self.tracked_time:
            return

        start_seconds =  self.start.strftime("%s")
        stop_seconds =  self.stop.strftime("%s")
        delta_seconds = self.delta()

        time_dir = os.path.join(self.project_dir, start_seconds)
        os.makedirs(time_dir, mode=0o700, exist_ok=True)
        filename = os.path.join(time_dir, "delta")

        with open(filename, "w") as fd:
            fd.write("%s\n" % delta_seconds)

    def delta(self, in_seconds=True):
        if self.tracked_time:
            delta = self.stop - self.start
        else:
            delta = datetime.timedelta()

        if in_seconds:
            delta = delta.total_seconds()

        return delta


class Report(object):
    """Create a report on tracked time"""

    def __init__(self, args):
        pass

    @staticmethod
    def default_dates():
        """Return default start and end of of time
        start: first of last month
        end: last of last month
        """

        now = datetime.datetime.now()
        first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = first_day - datetime.timedelta(days=1)
        start_date = end_date.replace(day=1)

        return (start_date, end_date)


# Setup locale for calendar printing
# Setup locale to get Timezone information?
#print(locale.getlocale())

# Record project
# Record tags

def cmd_track(args):
    """Command line handler for time tracking"""
    tracker = Tracker(args.project[0])
    tracker.track_time()
    tracker.write_time()
    print(tracker.delta())

def cmd_report(args):
    """Command line handler for time reporting"""
    #report = Report(args.project[0])
    print(Report.default_dates())

def parse_argv(argv):
    parser = {}
    parser['main'] = argparse.ArgumentParser(description='ctt ' + VERSION)
    parser['sub'] = parser['main'].add_subparsers(title="Commands")

    parser['track'] = parser['sub'].add_parser('track')
    parser['track'].set_defaults(func=cmd_track)
    parser['track'].add_argument("project", help="Project to track time for", nargs=1)

    parser['report'] = parser['sub'].add_parser('report')
    parser['report'].set_defaults(func=cmd_report)
    parser['report'].add_argument("project", help="Project to report time for", nargs=1)
    parser['report'].add_argument("-s", "--start", help="Start datetime (first of last month)", nargs=1)
    parser['report'].add_argument("-e", "--end", help="End datetime (last of last month)", nargs=1)

    #parser['track'].add_argument("-t", "--tag", help="Add tags",
    #    action="store_true")

    args = parser['main'].parse_args()
    print(args)

    args.func(args)

if __name__ == "__main__":
    parse_argv(sys.argv[1:])
    sys.exit(0)

# Setup signal handler
# Start tracking
# Save stuff to our home directory

# Create datetime from userinput
# Wed Aug  1 23:35:53 2012
