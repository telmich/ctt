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
import ctt.tracker as tr
import os
import datetime
import shutil

class TrackerTestCase(ctt.test.CttTestCase):
    def test___init__(self):
        project = 'foo1'
        expected_project_dir = os.path.join(ctt.test.fixtures_dir,
                os.path.join('.ctt', project))
        tracker = tr.Tracker(project)
        self.assertEqual(tracker.project, project)
        self.assertEqual(tracker.project_dir, expected_project_dir)
        self.assertIsNone(tracker.start_datetime)
        self.assertIsNone(tracker.end_datetime)
        self.assertIsNone(tracker.comment)
        self.assertFalse(tracker._tracked_time)

        tracker = tr.Tracker(project, start_datetime=('2016-04-09-0900',))
        self.assertEqual(tracker.start_datetime,
                datetime.datetime(2016, 4, 9, 9, 0))
        self.assertIsNone(tracker.end_datetime)
        self.assertFalse(tracker._tracked_time)

        tracker = tr.Tracker(project, start_datetime=('2016-04-04-0900',),
                end_datetime=('2016-04-09-2000',))
        self.assertEqual(tracker.start_datetime,
                datetime.datetime(2016, 4, 4, 9, 0))
        self.assertEqual(tracker.end_datetime,
                datetime.datetime(2016, 4, 9, 20, 0))
        self.assertTrue(tracker._tracked_time)

    @unittest.expectedFailure
    def test__init__fail(self):
        project = 'foo1'
        tracker = tr.Tracker(project, start_datetime=('2016-04-090900',))

    def test_delta(self):
        project = 'foo1'
        start_dt = datetime.datetime(2016, 4, 4, 9, 0)
        end_dt = datetime.datetime(2016, 4, 9, 20, 0)
        tracker = tr.Tracker(project, start_datetime=('2016-04-04-0900',),
                end_datetime=('2016-04-09-2000',))
        expected_delta = end_dt - start_dt
        tracker._tracked_time = True
        delta = tracker.delta(True)
        self.assertEqual(delta, expected_delta.total_seconds())
        delta = tracker.delta(False)
        self.assertEqual(delta, expected_delta)
        tracker._tracked_time = False
        delta = tracker.delta(True)
        self.assertEqual(delta, 0)
        delta = tracker.delta(False)
        self.assertEqual(delta, datetime.timedelta())

    def test_write_time(self):
        project = 'foo1'
        start_dt = '2016-04-09-1730'
        tracker = tr.Tracker(project, start_datetime=(start_dt,),
                comment=True)
        end_dt = datetime.datetime(2016, 4, 9, hour=17, minute=45)
        expected_delta = str(15 * 60) + '.0\n'  # seconds
        tracker.end_datetime = end_dt
        tracker._tracked_time = True
        expected_comment = "test"
        tracker.comment = expected_comment
        expected_comment += "\n"
        timedir = os.path.join(os.path.join(
            ctt.test.fixtures_dir, os.path.join('.ctt', project)),
            '2016-04-09-1730')
        if os.path.exists(timedir):
            shutil.rmtree(timedir)
        tracker.write_time()
        timefile = os.path.join(timedir, ctt.FILE_DELTA)
        self.assertTrue(os.path.exists(timefile))
        with open(timefile, "r") as f:
            delta = f.read()
        self.assertEqual(delta, expected_delta)
        commentfile = os.path.join(timedir, ctt.FILE_COMMENT)
        self.assertTrue(os.path.exists(commentfile))
        with open(commentfile, "r") as f:
            comment = f.read()
        self.assertEqual(comment, expected_comment)

    @unittest.expectedFailure
    def test_write_time_fail(self):
        project = 'foo1'
        start_dt = '2016-04-09-1730'
        tracker = tr.Tracker(project, start_datetime=(start_dt,),
                comment=True)
        end_dt = datetime.datetime(2016, 4, 9, hour=17, minute=45)
        expected_delta = 15 * 60  # seconds
        tracker.end_datetime = end_dt
        tracker._tracked_time = True
        expected_comment = "test"
        tracker.comment = expected_comment
        timedir = os.path.join(os.path.join(
            ctt.test.fixtures_dir, os.path.join('.ctt', project)),
            '2016-04-09-1730')
        if os.path.exists(timedir):
            shutil.rmtree(timedir)
        os.makedirs(timedir, mode=0o700)
        tracker.write_time()


if __name__ == '__main__':
    unittest.main()
