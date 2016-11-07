#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
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

import unittest
import ctt
import ctt.test
import ctt.report as report
import sys
from io import StringIO
import datetime
import collections


class ReportTestCase(ctt.test.CttTestCase):
    def setUp(self):
        super(ReportTestCase, self).setUp()
        self.sys_stdout = sys.stdout
        out = StringIO()
        sys.stdout = out
        self.maxDiff = None

    def _get_output(self):
        sys.stdout.flush()
        output = sys.stdout.getvalue().strip()
        return output

    def tearDown(self):
        sys.stdout = self.sys_stdout
        super(ReportTestCase, self).tearDown()

    def test_print_report_time_entries(self):
        report_data = {
            '2016-04-07-0826': [
                {
                'start_datetime': '2016-04-07-0826',
                'end_datetime': '2016-04-07-2359',
                'comment': 'foo1',
                'delta': '6',
                'delta_seconds': '6',
                'delta_minutes': '0',
                },
            ],
        }
        report.Report.print_report_time_entries(report_data, ctt.REPORTFORMAT,
                False)
        output = self._get_output()
        expected_output = "2016-04-07-0826 (6): foo1"
        self.assertEqual(output, expected_output)

    def test_print_report_time_entries_summary(self):
        report_data = {
            '2016-04-07-0826': [
                {
                'start_datetime': '2016-04-07-0826',
                'end_datetime': '2016-04-07-2359',
                'comment': 'foo1',
                'delta': '6',
                'delta_seconds': '6',
                'delta_minutes': '0',
                },
            ],
            '2016-04-07-0926': [
                {
                'start_datetime': '2016-04-07-0926',
                'end_datetime': '2016-04-07-2359',
                'comment': 'foo12',
                'delta': '10',
                'delta_seconds': '10',
                'delta_minutes': '0',
                },
            ],
        }
        report.Report.print_report_time_entries(report_data, ctt.REPORTFORMAT,
                True)
        output = self._get_output()
        expected_output = ("2016-04-07-0826 (6): foo1\n"
                "2016-04-07-0926 (10): foo12")
        self.assertEqual(output, expected_output)

    def test_print_reports(self):
        reports = collections.OrderedDict()
        for project in ('foo1', 'foo2'):
            rep = report.Report(project, ('2016-04-07',), ('2016-04-08',),
                    ctt.REPORTFORMAT, None, None)
            report_data = rep.report()
            reports[project] = (rep, report_data)
        expected_output = (
            "Report for foo1 between 2016-04-07 00:00:00 and 2016-04-08 23:59:59\n"
            "2016-04-07-0826 (0:00:06): foo1\n"
            "2016-04-08-1200 (1:23:20): foo1 12\n"
            "Report for foo2 between 2016-04-07 00:00:00 and 2016-04-08 23:59:59\n"
            "2016-04-07-0810 (0:00:10): foo2"
        )
        rep.print_reports(reports, ctt.REPORTFORMAT, summary=False)
        output = self._get_output()
        self.assertEqual(output, expected_output)

    # Summary should not print time entries
    # def test_print_reports_summary(self):
    #     reports = collections.OrderedDict()
    #     for project in ('foo1', 'foo2'):
    #         rep = report.Report(project, ('2016-04-07',), ('2016-04-08',),
    #                 ctt.REPORTFORMAT, None, None)
    #         report_data = rep.report()
    #         reports[project] = (rep, report_data)
    #     expected_output = (
    #         "2016-04-07-0810 (0:00:10): foo2\n"
    #         "2016-04-07-0826 (0:00:06): foo1\n"
    #         "2016-04-08-1200 (1:23:20): foo1 12"
    #     )
    #     rep.print_reports(reports, ctt.REPORTFORMAT, summary=True)
    #     output = self._get_output()
    #     self.assertEqual(output, expected_output)

    def test__init_date(self):
        rep = report.Report('foo1', ('2016-04-07',), ('2016-04-07',),
                ctt.REPORTFORMAT, None, None)
        expected_start_date = datetime.datetime(2016, 4, 7)
        expected_end_date = datetime.datetime(2016, 4, 7, 23, 59, 59)
        self.assertEqual(rep.start_date, expected_start_date)
        self.assertEqual(rep.end_date, expected_end_date)

    @unittest.expectedFailure
    def test__init_date_fail(self):
        rep = report.Report('foo1', ('2016-04-08',), ('2016-04-07',),
                ctt.REPORTFORMAT, None, None)

    def test__init_date_defaults(self):
        rep = report.Report('foo1', None, None,
                ctt.REPORTFORMAT, None, None)
        now = datetime.datetime.now()
        expected_start_date = now.replace(day=1, hour=0, minute=0, second=0,
                microsecond=0)
        next_month = expected_start_date.replace(day=28) + datetime.timedelta(days=4)
        first_day_next_month = next_month.replace(day=1)
        expected_end_date = first_day_next_month - datetime.timedelta(seconds=1)
        self.assertEqual(rep.start_date, expected_start_date)
        self.assertEqual(rep.end_date, expected_end_date)

    @unittest.expectedFailure
    def test__init_report_db_fail(self):
        rep = report.Report('unexisting', ('2016-04-07',), ('2016-04-07',),
                ctt.REPORTFORMAT, None, None)

    def test__init_report_db(self):
        rep = report.Report('foo1', ('2016-04-07',), ('2016-04-07',),
                ctt.REPORTFORMAT, None, None)
        expected_db =  {
                '2016-04-07-0826': {
                    'comment': 'foo1',
                    'delta': '6.248274'
                },
        }
        self.assertEqual(rep._report_db, expected_db)

    def test_header(self):
        rep = report.Report('foo1', ('2016-04-07',), ('2016-04-07',),
                ctt.REPORTFORMAT, None, None)
        rep.header()
        output = self._get_output()
        self.assertEqual(output, ("Report for foo1 between 2016-04-07 00:00:00"
            " and 2016-04-07 23:59:59"))

    def test_summary(self):
        report.Report.summary(10)
        output = self._get_output()
        self.assertEqual(output, "Total time tracked: 0h 0m 10s.")

    def test_total_time(self):
        rep = report.Report('foo1', ('2016-04-07',), ('2016-04-07',),
                ctt.REPORTFORMAT, None, None)
        total_time = rep.total_time
        expected_total_time =  6.248274
        self.assertEqual(total_time, expected_total_time)

    def test_report(self):
        rep = report.Report('foo1', ('2016-04-07',), ('2016-04-08',),
                ctt.REPORTFORMAT, None, None)
        expected_entries = {
                '2016-04-07-0826': [
                    {
                    'start_datetime': '2016-04-07-0826',
                    'end_datetime': '2016-04-07-0826',
                    'comment': 'foo1',
                    'delta': datetime.timedelta(seconds=6),
                    'delta_seconds': 6,
                    'delta_minutes': 0,
                    },
                ],
                '2016-04-08-1200': [
                    {
                    'start_datetime': '2016-04-08-1200',
                    'end_datetime': '2016-04-08-1323',
                    'comment': 'foo1 12',
                    'delta': datetime.timedelta(seconds=5000),
                    'delta_seconds': 5000,
                    'delta_minutes': 83,
                    },
                ],
        }
        entries = rep.report()
        self.assertEqual(entries, expected_entries)


if __name__ == '__main__':
    unittest.main()
