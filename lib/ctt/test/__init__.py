# -*- coding: utf-8 -*-
#
# 2016 Darko Poljak (darko.poljak at gmail.com))
#
# This file is part of ctt.
#
# cdist is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cdist is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cdist. If not, see <http://www.gnu.org/licenses/>.
#
#

import os
import unittest

fixtures_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "fixtures"))

class CttTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['HOME'] = fixtures_dir
