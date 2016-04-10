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

import unittest
import ctt
import ctt.listprojects as cttls
import ctt.test

class ListProjectsTestCase(ctt.test.CttTestCase):

    def test_list_projects(self):
        projects = cttls.ListProjects.list_projects()
        expected_projects = [ 'foo1', 'foo2', 'foo3', 'spam-eggs',
                'test-1', 'test-2', 'test-3', ]
        gotten_projects = sorted(projects)
        self.assertEqual(gotten_projects, expected_projects)

if __name__ == '__main__':
    unittest.main()
