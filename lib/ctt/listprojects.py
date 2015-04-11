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

import ctt
import logging
import os

log = logging.getLogger(__name__)

class ListProjects(object):
    """Return existing projects"""

    @classmethod
    def commandline(cls, args):
        cls.print_projects()


    @classmethod
    def print_projects(cls):
        for project in cls.list_projects():
            print(project)

    @staticmethod
    def list_projects():
        for project in sorted(os.listdir(ctt.ctt_dir())):
            if project[0] == ".":
                continue

            yield project
