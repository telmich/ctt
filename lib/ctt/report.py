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

import datetime

import logging

import os
import os.path
import re
import glob
import collections

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
            projects = ctt.listprojects.ListProjects.list_projects()

        else:
            projects = []
            for x in args.project:
                fnames = glob.glob(os.path.join(ctt.ctt_dir(), x))
                projects.extend(fnames)

        total_time = 0
        reports = collections.OrderedDict()
        for project in projects:
            report = cls(project=project, start_date=args.start,
                         end_date=args.end, output_format=args.output_format,
                         regexp=args.regexp, ignore_case=args.ignore_case)
            report_data = report.report()
            reports[report.project] = (report, report_data)
            total_time = total_time + report.total_time
        cls.print_reports(reports, args.output_format, args.summary)

        cls.summary(total_time)

    @staticmethod
    def print_report_time_entries(report_data, output_format, summary):
        ''' Print time entries from report_data report using output_format.
        '''
        keys = sorted(report_data.keys())
        for time in keys:
            entries = report_data[time]
            for entry in entries:
                print(output_format.format_map(entry))

    @staticmethod
    def print_reports(reports, output_format, summary):
        ''' Print reports using output_format for each entry.

            If summary is True then all time entries from all
            projects is extracted to one report dict.
            Otherwise, all time entries by each project is printed.
        '''
        if summary:
            summary_report = {}
        for project in reports:
            report, report_data = reports[project]
            if summary:
                for time in report_data:
                    if time not in summary_report:
                        summary_report[time] = report_data[time]
                    else:
                        summary_report[time].extend(report_data[time])
            else:
                report.header()
                Report.print_report_time_entries(report_data,
                                                 output_format, summary)
        # For summary do not print time entries.
        # if summary:
        #     Report.print_report_time_entries(summary_report,
        #             output_format, summary)

    def _init_date(self, start_date, end_date):
        """Setup date - either default or user given values"""

        now = datetime.datetime.now()
        first_day_this_month = now.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = first_day_this_month.replace(
            day=28) + datetime.timedelta(days=4)
        first_day_next_month = next_month.replace(day=1)
        last_day_this_month = first_day_next_month - datetime.timedelta(
            seconds=1)

        default_start_date = first_day_this_month
        default_end_date = last_day_this_month

        # default_end_date = first_day - datetime.timedelta(days=1)
        # default_start_date = default_end_date.replace(day=1)

        try:
            if start_date:
                self.start_date = datetime.datetime.strptime(
                    start_date[0], ctt.DATEFORMAT)
            else:
                self.start_date = default_start_date

            if end_date:
                self.end_date = datetime.datetime.strptime(
                    end_date[0], ctt.DATEFORMAT)
            else:
                self.end_date = default_end_date
        except ValueError as e:
            raise ctt.Error(e)

        self.end_date = self.end_date.replace(
            hour=23, minute=59, second=59)

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
                dir_datetime = datetime.datetime.strptime(
                    dirname, ctt.DISKFORMAT)
            except ValueError:
                log.warning("Invalid time entry {entry} for project "
                            "{project}, skipping.".format(
                                entry=dirname, project=self.project))
                continue

            if (dir_datetime >= self.start_date and
                    dir_datetime <= self.end_date):
                filename = os.path.join(
                    self.project_dir, dirname, ctt.FILE_DELTA)
                comment_filename = os.path.join(
                    self.project_dir, dirname, ctt.FILE_COMMENT)

                # Check for matching comment
                comment = None
                if os.path.exists(comment_filename):
                    with open(comment_filename, "r") as fd:
                        comment = fd.read().rstrip('\n')

                    # If regular expression given, but not matching, skip entry
                    if (self.regexp and
                            not re.search(self.regexp, comment,
                                          self.search_flags)):
                        continue

                self._report_db[dirname] = {}
                if comment:
                    self._report_db[dirname]['comment'] = comment

                with open(filename, "r") as fd:
                    self._report_db[dirname]['delta'] = fd.read().rstrip('\n')

                log.debug("Recording: %s: %s"
                          % (dirname, self._report_db[dirname]['delta']))

            else:
                log.debug("Skipping: %s" % dirname)

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
        ''' Get one time entry data.
        '''
        report = {}
        start_datetime = datetime.datetime.strptime(time, ctt.DATETIMEFORMAT)
        delta = datetime.timedelta(seconds=int(float(entry['delta'])))
        end_datetime = (start_datetime + delta).replace(microsecond=0)

        report['start_datetime'] = start_datetime.strftime(ctt.DATETIMEFORMAT)
        report['end_datetime'] = end_datetime.strftime(ctt.DATETIMEFORMAT)

        report['delta'] = delta
        report['delta_seconds'] = int(float(entry['delta']))
        report['delta_minutes'] = int(report['delta_seconds']/60)

        if 'comment' in entry:
            report['comment'] = entry['comment']
        else:
            report['comment'] = False
        return report

    def report(self):
        """Return total time tracked"""

        entries = {}
        time_keys = self._report_db.keys()
        for time in time_keys:
            entry = self._report_db[time]
            report = self._get_report_entry(time, entry)
            if time not in entries:
                entries[time] = [report]
            else:
                entries[time].append(report)
        return entries
