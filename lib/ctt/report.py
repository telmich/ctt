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

log = logging.getLogger(__name__)

class Report(object):
    """Create a report on tracked time"""

    def __init__(self, project, start_date, end_date):

        # Setup default values
        if not start_date and not end_date:
            start_date, end_date = self.default_dates()

        self.start_seconds = start_date.strftime("%s")
        self.end_seconds = end_date.strftime("%s")

        self.project = project
        self.project_dir = project_dir(self.project)

        self._init_report_db()

    def _init_report_db(self):
        """Read all contents from db"""

        self._report_db = {}
        for dirname in os.listdir(self.project_dir):
            print("%s:%s:%s" % (self.start_seconds, dirname, self.end_seconds))
            if dirname >= self.start_seconds and dirname <= self.end_seconds:
                filename = os.path.join(self.project_dir, dirname, FILE_DELTA)
                with open(filename, "r") as fd:
                    self._report_db[dirname] = fd.read().rstrip('\n')

                print("%s: %s" % (dirname, self._report_db[dirname]))

    def total_time(self):
        """Return total time tracked"""
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
