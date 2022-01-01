# HexwarePy is a Python library of utilities that its author
# found useful for general Python development, arranged
# to function like an extension to the language.
# Modules vary greatly with respect to which types of projects
# they assist with.
# Copyright notice for this file:
#  Copyright 2021 Hextator

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# https://www.gnu.org/licenses/gpl-3.0.en.html

# Provides additional functions for managing threads

import threading

def createDaemonThread(targ, threadArgs = None, threadKWargs = None):
	threadArgs = () if threadArgs is None else threadArgs
	threadKWargs = {} if threadKWargs is None else threadKWargs
	output = threading.Thread(target = targ, args = threadArgs, kwargs = threadKWargs)
	output.daemon = True
	output.start()
	return output
