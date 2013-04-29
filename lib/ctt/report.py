#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 2012 Nico Schottelius (nico-ctt at schottelius.org)
#
# This file is part of ctt.
#
# ctt is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ctt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ctt. If not, see <http://www.gnu.org/licenses/>.
#
#

import calendar
import datetime

import logging
import time

import os
import os.path
import re
import sys

import ctt

log = logging.getLogger(__name__)

class Report(object):
    """Create a report on tracked time"""

    def __init__(self, project, start_date, end_date, 
        output_format, regexp, ignore_case):

        self.project = project
        self.project_dir = ctt.project_dir(self.project)

        self.output_format = output_format
        self.regexp = regexp

        if ignore_case:
            self.search_flags = re.IGNORECASE
        else:
            self.search_flags = 0

        self._init_date(start_date, end_date)
        self._init_report_db()

    @classmethod
    def commandline(cls, args):
        report = cls(args.project[0], args.start, args.end, args.output_format, args.regexp, args.ignore_case)
        report.report()


    def _init_date(self, start_date, end_date):
        """Setup date - either default or user given values"""


        now = datetime.datetime.now()
        first_day_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = first_day_this_month.replace(day=28) + datetime.timedelta(days=4)
        first_day_next_month = next_month.replace(day=1)
        last_day_this_month = first_day_next_month - datetime.timedelta(seconds=1)

        default_start_date = first_day_this_month
        default_end_date = last_day_this_month

        #default_end_date = first_day - datetime.timedelta(days=1)
        #default_start_date = default_end_date.replace(day=1)

        try:
            if start_date:
                self.start_date = datetime.datetime.strptime(start_date[0], ctt.DATEFORMAT)
            else:
                self.start_date = default_start_date

            if end_date:
                self.end_date = datetime.datetime.strptime(end_date[0], ctt.DATEFORMAT)
            else:
                self.end_date = default_end_date
        except ValueError as e:
            raise ctt.Error(e)

        self.end_date = self.end_date.replace(hour=23,minute=59,second=59)

        if self.start_date >= self.end_date:
            raise ctt.Error("End date must be after start date (%s >= %s)" % 
                (self.start_date, self.end_date))

    def _init_report_db(self):
        """Read all contents from db"""

        if not os.path.isdir(self.project_dir):
            raise ctt.Error("Project does not exist: %s" % (self.project))

        self._report_db = {}
        for dirname in os.listdir(self.project_dir):
            dir_datetime = datetime.datetime.strptime(dirname, ctt.DISKFORMAT)
            if dir_datetime >= self.start_date and dir_datetime <= self.end_date:
                filename = os.path.join(self.project_dir, dirname, ctt.FILE_DELTA)
                comment_filename = os.path.join(self.project_dir, dirname, ctt.FILE_COMMENT)

                # Check for matching comment
                comment = None
                if os.path.exists(comment_filename):
                    with open(comment_filename, "r") as fd:
                        comment = fd.read().rstrip('\n')
                    
                    # If regular expression given, but not matching, skip entry
                    if self.regexp and not re.search(self.regexp, comment, self.search_flags):
                        continue


                self._report_db[dirname] = {}
                if comment:
                    self._report_db[dirname]['comment'] = comment

                with open(filename, "r") as fd:
                    self._report_db[dirname]['delta'] = fd.read().rstrip('\n')

                log.debug("Recording: %s: %s" % (dirname, self._report_db[dirname]['delta']))

            else:
                log.debug("Skipping: %s" % dirname)

    def report(self):
        self.list_entries()
        self.summary()

    def summary(self):
        """Show report to the user"""

        hours, minutes, seconds = ctt.user_timedelta(self.total_time()) 

        print("Tracked time between %s and %s: %sh %sm %ss." %
            (self.start_date, self.end_date, hours, minutes, seconds))

    def total_time(self):
        """Return all entries"""

        count = 0
        for entry in self._report_db.values():
            delta = entry['delta']
            log.debug("Adding %s to %s time..." % (delta, count))
            count = count + float(delta)

        return count


    def list_entries(self):
        """Return total time tracked"""

        sorted_times = sorted(self._report_db.keys())
        #for time, entry in self._report_db.items():

        for time in sorted_times:
            entry = self._report_db[time]
            report = {}

            report['start_datetime'] = datetime.datetime.strptime(time, ctt.DATETIMEFORMAT)

            report['delta_seconds'] = int(float(entry['delta']))
            report['delta_minutes'] = int(report['delta_seconds']/60)
            report['delta'] = datetime.timedelta(seconds=int(float(entry['delta'])))
            report['end_datetime'] = (report['start_datetime'] + report['delta']).replace(microsecond = 0)

            if 'comment' in entry:
                report['comment'] = entry['comment']
            else:
                report['comment'] = False

            print(self.output_format.format_map(report))
