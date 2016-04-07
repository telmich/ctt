#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 2012 Nico Schottelius (nico-ctt at schottelius.org)
# 2016 Darko Poljak (darko.poljak at gmail.com)
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
import glob

import ctt
import ctt.listprojects

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
        # Report time for all projects
        if args.all:
            projects=ctt.listprojects.ListProjects.list_projects()

        else:
            projects = []
            for x in args.project:
                fnames = glob.glob(os.path.join(ctt.ctt_dir(), x))
                projects.extend(fnames)

        total_time = 0
        entries = {}
        for project in projects:
            report = cls(project=project, start_date=args.start,
                    end_date=args.end, output_format=args.output_format,
                    regexp=args.regexp, ignore_case=args.ignore_case)
            project_report = report.report(args.summary)
            if args.summary:
                cls.update_summary_report(entries, project_report)
            else:
                report.print_report(project_report, args.output_format)
            total_time = total_time + report.total_time
        if args.summary:
            cls.print_summary_report(entries, args.output_format)

        cls.summary(total_time)


    @staticmethod
    def update_summary_report(report, entry):
        for time in entry:
            if not time in report:
                report[time] = []
            report[time].extend(entry[time])


    @staticmethod
    def print_summary_report(report, output_format):
        Report.print_report_entries(report, output_format, sorted_keys=True)

    @staticmethod
    def print_report_entries(report, output_format, sorted_keys=False):
        if sorted_keys:
            keys = sorted(report.keys())
        else:
            keys = report.keys()
        for time in keys:
            entries = report[time]
            for entry in entries:
                print(output_format.format_map(entry))

    def print_report(self, report, output_format):
        self.header()
        self.print_report_entries(report, output_format)

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
            log.debug("Dirname: %s" % dirname)
            try:
                dir_datetime = datetime.datetime.strptime(dirname, ctt.DISKFORMAT)
            except ValueError:
                raise ctt.Error("Invalid time entry {entry} for project {project}, aborting!".format(entry=dirname, project=self.project))

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

    def report(self, summary=False):
        return self.list_entries()

    def header(self):
        project_name = os.path.basename(self.project)
        print("Report for %s between %s and %s" %
            (project_name, self.start_date, self.end_date))

    @staticmethod
    def summary(total_time):
        hours, minutes, seconds = ctt.user_timedelta(total_time) 

        print("Total time tracked: %sh %sm %ss." %
            (hours, minutes, seconds))

    @property
    def total_time(self):
        """Return all entries"""

        count = 0
        for entry in self._report_db.values():
            delta = entry['delta']
            log.debug("Adding %s to %s time..." % (delta, count))
            count = count + float(delta)

        return count


    def _get_report_entry(self, time, entry):
        report = {}
        start_datetime  = datetime.datetime.strptime(time, ctt.DATETIMEFORMAT)
        delta = datetime.timedelta(seconds=int(float(entry['delta'])))
        end_datetime    = (start_datetime + delta).replace(microsecond = 0)

        report['start_datetime'] = start_datetime.strftime(ctt.DATETIMEFORMAT)
        report['end_datetime']   = end_datetime.strftime(ctt.DATETIMEFORMAT)

        report['delta'] = delta
        report['delta_seconds'] = int(float(entry['delta']))
        report['delta_minutes'] = int(report['delta_seconds']/60)

        if 'comment' in entry:
            report['comment'] = entry['comment']
        else:
            report['comment'] = False
        return report


    def list_entries(self):
        """Return total time tracked"""

        entries = {}
        time_keys = self._report_db.keys()
        for time in time_keys:
            entry = self._report_db[time]
            report = self._get_report_entry(time, entry)
            if not time in entries:
                entries[time] = []
            entries[time].append(report)
        return entries
