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

import os
import os.path

VERSION         = "0.1"
FILE_DELTA      = "delta"
DATEFORMAT      = "%Y-%m-%d"

class Error(Exception):
    pass

# Our output format
def user_datetime(when):
    """Print time for the user"""
    return when.ctime()

def project_dir(project):
    home = os.environ['HOME']
    ctt_dir = os.path.join(home, ".ctt")
    project_dir = os.path.join(ctt_dir, project)

    return project_dir
