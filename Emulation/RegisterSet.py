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

import Logging

class RegisterSet():
	def __init__(self, debugRegisters = False, onUpdate = None, onRead = None):
		self.registers = {}

		self.debugRegisters = debugRegisters
		self.onUpdate = onUpdate
		self.onRead = onRead

	def __getitem__(self, key):
		register, dataType, name = key
		data = self.registers[register]
		value, expectedType, oldName, lineNum = data
		if self.onRead:
			self.onRead(register, data)
		if self.debugRegisters and dataType != expectedType:
			raise Exception(
				'Type mismatch when referencing data from line ' + str(lineNum) + ':\nvariable ' + name +
				' does not match the expected type of the variable ' + oldName +
				'\n(Old type was ' + expectedType + '; new type was ' + dataType + ')'
			)
		return value

	def __setitem__(self, key, value):
		register, dataType, name = key
		lineNum = '[Unknown Line Number]'
		if self.debugRegisters:
			lineNum = Logging.callInfo(2).lineno
		data = (value, dataType, name, lineNum)
		if self.onUpdate:
			oldData = None
			if register in self.registers:
				oldData = self.registers[register]
			self.onUpdate(register, oldData, data)
		self.registers[register] = data

	def __repr__(self):
		return repr(self.registers)

	def printReg(self, register):
		value, dataType, name, lineNum = self.registers[register]
		print(register + ' set by line ' + str(lineNum) + ' via ' + name + ' = (' + dataType + ')' + str(value))
