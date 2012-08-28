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
import sys

import ctt

log = logging.getLogger(__name__)

class Report(object):
    """Create a report on tracked time"""

    def __init__(self, project, start_date, end_date):

        # Setup default values
        try:
            if start_date:
                self.start_date = datetime.datetime.strptime(start_date[0], ctt.DATEFORMAT)
            else:
                self.start_date = self.default_dates()[0]

            if end_date:
                self.end_date = datetime.datetime.strptime(end_date[0], ctt.DATEFORMAT)
            else:
                self.end_date = self.default_dates()[1]
        except ValueError as e:
            raise ctt.Error(e)

        self.start_seconds  = self.start_date.strftime("%s")
        self.end_seconds    = self.end_date.strftime("%s")

        self.project = project
        self.project_dir = ctt.project_dir(self.project)

        self._init_report_db()

    @classmethod
    def commandline(cls, args):
        report = cls(args.project[0], args.start, args.end)
        report.report()

    def _init_report_db(self):
        """Read all contents from db"""

        if not os.path.isdir(self.project_dir):
            raise ctt.Error("Project does not exist: %s" % (self.project))

        self._report_db = {}
        for dirname in os.listdir(self.project_dir):
            dir_datetime = datetime.datetime.strptime(dirname, ctt.DISKFORMAT)
            if dir_datetime >= self.start_date and dir_datetime <= self.end_date:
                filename = os.path.join(self.project_dir, dirname, ctt.FILE_DELTA)
                with open(filename, "r") as fd:
                    self._report_db[dirname] = fd.read().rstrip('\n')

                log.debug("Recording: %s: %s" % (dirname, self._report_db[dirname]))
            else:
                log.debug("Skipping: %s" % dirname)

    def report(self):
        """Show report to the user"""

        hours, minutes, seconds = ctt.user_timedelta(self.total_time()) 

        print("Tracked time between %s and %s: %sh %sm %ss." %
            (self.start_date, self.end_date, hours, minutes, seconds))

    def total_time(self):
        """Return total time tracked"""

        count = 0
        for times in self._report_db.values():
            log.debug("Adding %s to %s time..." % (times, count))
            count = count + float(times)

        return count


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
