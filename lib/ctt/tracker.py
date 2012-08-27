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
    def __init__(self, project):
        self.project = project
        self.tracked_time = False

        self.project_dir = ctt.project_dir(project)

    @classmethod
    def commandline(cls, args):
        tracker = cls(args.project[0])
        tracker.track_time()
        tracker.write_time()
        log.info(tracker.delta())

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
        filename = os.path.join(time_dir, ctt.FILE_DELTA)

        with open(filename, "w") as fd:
            fd.write("%s\n" % delta_seconds)

    def delta(self, in_seconds=True):
        """Return time delta - empty (==0) if not tracked"""

        if self.tracked_time:
            delta = self.stop - self.start
        else:
            delta = datetime.timedelta()

        if in_seconds:
            delta = delta.total_seconds()

        return delta
