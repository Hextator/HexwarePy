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

import functools

import struct

#UINT32_MAX = (1 << 32) - 1

def rawToFloat(intVal):
	#global UINT32_MAX

	#if (UINT32_MAX + 1) >> 1 <= intVal:
	#	intVal = (UINT32_MAX + 1) - intVal
	return struct.unpack('f', struct.pack('i', intVal))[0]

def floatToRaw(floatVal):
	#global UINT32_MAX

	intVal = struct.unpack('i', struct.pack('f', floatVal))[0]
	#if (UINT32_MAX + 1) >> 1 <= intVal:
	#	intVal = (UINT32_MAX + 1) - intVal
	return intVal

# TODO: Is this needed?
# DISABLED_XXX: This won't even work anyway if results seen prior were understood correctly
def asIEEE754F32(floatVal):
	return rawToFloat(floatToRaw(floatVal))
	#return floatVal

@functools.total_ordering
class LowFloat32():
	def __init__(self, rawInt):
		self.data = rawToFloat(rawInt)

	def __neg__(self):
		result = LowFloat32(0)
		result.data = asIEEE754F32(-self.data)
		return result

	def __add__(self, other):
		result = LowFloat32(0)
		result.data = asIEEE754F32(self.data + other.data)
		return result

	def __sub__(self, other):
		result = LowFloat32(0)
		result.data = asIEEE754F32(self.data - other.data)
		return result

	def __mul__(self, other):
		result = LowFloat32(0)
		result.data = asIEEE754F32(self.data * other.data)
		return result

	def __truediv__(self, other):
		result = LowFloat32(0)
		result.data = asIEEE754F32(self.data/other.data)
		return result

	def __eq__(self, other):
		return self.data == other.data

	def __lt__(self, other):
		return self.data < other.data

	def __str__(self):
		outStr = str(self.data) + ' '
		asHex = '0x%08X' % self.asRaw()
		return outStr + '(' + asHex + ')'

	def trunc(self):
		self.data = int(self.data)
		return self

	def asRaw(self):
		return floatToRaw(self.data)

	def asHigh(self):
		return self.data
