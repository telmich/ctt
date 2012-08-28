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

import datetime
import logging
import time
import os
import os.path
import sys

import ctt

log = logging.getLogger(__name__)

class Tracker:
    def __init__(self, project, start_datetime = None, end_datetime = None, comment = False):
        self.project = project
        self.project_dir = ctt.project_dir(project)

        self._tracked_time = False
        self.comment = None

        # Setup default values
        try:
            if start_datetime:
                self.start_datetime = datetime.datetime.strptime(start_datetime[0], ctt.DATETIMEFORMAT)
            else:
                self.start_datetime = None

            if end_datetime:
                self.end_datetime = datetime.datetime.strptime(end_datetime[0], ctt.DATETIMEFORMAT)
            else:
                self.end_datetime = None
        except ValueError as e:
            raise ctt.Error(e)

        if self.start_datetime and self.end_datetime:
            self._tracked_time = True


    @classmethod
    def commandline(cls, args):
        tracker = cls(args.project[0], args.start, args.end, args.comment)
        tracker.track_time()

        if args.comment:
            tracker.record_comment()

        tracker.write_time()
        log.info(tracker.delta())

    def record_comment(self):
        """Record a comment for tracked data"""
        self.comment = input("Comment: ")

    # Track time and return information from tracking
    def track_time(self):
        """Track time, if necessary"""

        # Do not track again
        if self._tracked_time:
            return

        # If not given by the user
        if not self.start_datetime:
            self.start_datetime = datetime.datetime.now()

        try:
            # Wait for the exception to pop up
            input()
        except KeyboardInterrupt:
            pass

        self.end_datetime = datetime.datetime.now()

        self._tracked_time = True

    def write_time(self):
        if not self._tracked_time:
            return

        if self.start_datetime >= self.end_datetime:
            raise ctt.Error("End date must be after start date! (%s > %s)!" %
                (self.start_datetime, self.end_datetime))

        subdirname = self.start_datetime.strftime(ctt.DISKFORMAT)
        time_dir = os.path.join(self.project_dir, subdirname)

        if os.path.exists(time_dir):
            raise ctt.Error("Already tracked time at this beginning for this project")

        os.makedirs(time_dir, mode=0o700)
        filename = os.path.join(time_dir, ctt.FILE_DELTA)

        with open(filename, "w") as fd:
            fd.write("%s\n" % self.delta())

        if self.comment:
            filename = os.path.join(time_dir, ctt.FILE_COMMENT)
            with open(filename, "w") as fd:
                fd.write("%s\n" % self.comment)

    def delta(self, in_seconds=True):
        """Return time delta - empty (==0) if not tracked"""

        if self._tracked_time:
            delta = self.end_datetime - self.start_datetime
        else:
            delta = datetime.timedelta()

        if in_seconds:
            delta = delta.total_seconds()

        return delta
