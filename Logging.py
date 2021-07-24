# HexwarePy is a Python library of utilities that its author
# found useful for general Python development, arranged
# to function like an extension to the language.
# Modules vary greatly with respect to which types of projects
# they assist with.
# Copyright notice for this file:
#  Copyright 2021 Hextator

# Tested with Python 3.7

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

import inspect

def callInfo(depth):
	return inspect.getframeinfo(inspect.stack()[depth][0])

class PrintLogger():
	def __init__(self, loggingPath = None, alwaysPrint = False):
		self.logPath = loggingPath
		self.logEntries = []
		self.logWritten = False
		self.printAnyway = alwaysPrint

	def log(self, string):
		self.logEntries.append(string + '\n')
		if not self.logPath or self.printAnyway:
			print(string)

	def logEx(self, exType, message):
		self.log(exType.__name__ + ': ' + message)
		raise exType(message)

	def assertOrRaise(self, condition, exType, message):
		if not condition:
			self.logEx(exType, message)

	def writeLog(self):
		if self.logPath:
			with open(self.logPath, 'w') as logFile:
				for entry in self.logEntries:
					logFile.write(entry)

	def __enter__(self):
		return self

	def __exit__(self):
		if not self.logWritten:
			self.writeLog()
			self.logWritten = True

	# TOMAYBE: Is this worth having? It can cause problems...
	#def __del__(self):
	#	self.__exit__()
