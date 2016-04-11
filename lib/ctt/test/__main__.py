#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# 2016 Darko Poljak (darko.poljak at gmail.com)
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
# along with ctt. If not, see <http://www.gnu.org/licenses/>.
#
#

import imp
import os
import os.path
import sys
import unittest

base_dir = os.path.dirname(os.path.realpath(__file__))

test_modules = []
for possible_test in os.listdir(base_dir):
    if possible_test.startswith('test_'):
        mod_path = os.path.join(base_dir, possible_test)
        if os.path.isfile(mod_path):
            module = os.path.splitext(os.path.basename(possible_test))[0]
            test_modules.append(module)

suites = []
for test_module in test_modules:
    module_parameters = imp.find_module(test_module, [base_dir])
    module = imp.load_module("ctt.test." + test_module, *module_parameters)

    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    suites.append(suite)

all_suites = unittest.TestSuite(suites)
unittest.TextTestRunner(verbosity=2).run(all_suites)
