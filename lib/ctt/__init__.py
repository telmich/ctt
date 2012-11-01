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

VERSION         = "0.5"
FILE_DELTA      = "delta"
FILE_COMMENT    = "comment"
DATEFORMAT      = "%Y-%m-%d"
DATEFORMAT_PLAIN= DATEFORMAT.replace("%","")
DATETIMEFORMAT      = "%Y-%m-%d-%H%M"
DATETIMEFORMAT_PLAIN= DATETIMEFORMAT.replace("%","")

# Name of the folder to create - should not contain special characters
# to ensure cross-os compatibility
DISKFORMAT      = DATETIMEFORMAT

class Error(Exception):
    pass

# Our output format
def user_timedelta(seconds):
    """Format timedelta for the user"""

    if seconds >= 3600:
        hours = int(seconds / 3600)
        seconds = seconds - (hours * 3600)
    else:
        hours = 0

    if seconds >= 60:
        minutes = int(seconds / 60)
        seconds = seconds - (minutes * 60)
    else:
        minutes = 0

    return (hours, minutes, seconds)

def project_dir(project):
    home = os.environ['HOME']
    ctt_dir = os.path.join(home, ".ctt")
    project_dir = os.path.join(ctt_dir, project)

    return project_dir
