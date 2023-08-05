#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
#
# Copyright © 2003 - 2018 Michal Čihař <michal@cihar.com>
#
# This file is part of python-gammu <https://wammu.eu/python-gammu/>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from __future__ import print_function
import gammu
import sys

# Create object for talking with phone
state_machine = gammu.StateMachine()

# Read the configuration (~/.gammurc or from command line)
if len(sys.argv) > 2:
    state_machine.ReadConfig(Filename=sys.argv[1])
    del sys.argv[1]
else:
    state_machine.ReadConfig()

# Connect to the phone
state_machine.Init()

# Check whether we have a number to dial
if len(sys.argv) != 2:
    print('Usage: dialvoice.py NUMBER')
    sys.exit(1)

# Dial a number
state_machine.DialVoice(sys.argv[1])
