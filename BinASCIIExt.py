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

# Provides functions for representing binary data

import binascii
import re

# Map ASCII identifiers to their values

NUL = 0x00
SOH = 0x01
STX = 0x02
ETX = 0x03
EOT = 0x04
ENQ = 0x05
ACK = 0x06
BEL = 0x07
BS  = 0x08
TAB = 0x09
LF  = 0x0A
VT  = 0x0B
FF  = 0x0C
CR  = 0x0D
SO  = 0x0E
SI  = 0x0F
DLE = 0x10
DC1 = 0x11
DC2 = 0x12
DC3 = 0x13
DC4 = 0x14
NAK = 0x15
SYN = 0x16
ETB = 0x17
CAN = 0x18
EM  = 0x19
SUB = 0x1A
ESC = 0x1B
FS  = 0x1C
GS  = 0x1D
RS  = 0x1E
US  = 0x1F
DEL = 0x7F

__escaped__ = re.compile('(\\\\x[0-9a-fA-F]{2})')
def readableBytes(inBytes):
	rep = repr(inBytes)[2:-1]
	split = __escaped__.split(rep)
	rep = '"'
	for string in split:
		if __escaped__.match(string):
			string = '"[' + string[2:].upper() + ']"'
		rep += string
	rep += '"'
	rep = rep.replace(']""[', '][')
	if rep.startswith('""'):
		rep = rep[2:]
	if rep.endswith('""'):
		rep = rep[0:-2]
	return rep

def spaceDelimitBytes(byteString):
	originalInput = byteString
	outString = ''
	while byteString:
		curr = byteString[0:2]
		byteString = byteString[2:]
		try:
			int('0x' + curr, 0)
		except:
			return originalInput
		outString += curr + ' '
	return outString[0:-1]

def encodeUpper(toEncode):
	"""Performs hexadecimal encoding with uppercase characters"""
	return spaceDelimitBytes(str(binascii.hexlify(stringToBytes(toEncode)))[2:-1].upper())

def asHexString(toEncode):
	"""Converts a list of integers used as 8 bit values
	to a hexadecimal string with uppercase characters;
	also works on bytes objects"""
	return (''.join(('%02X ' % x) for x in toEncode)).rstrip()

def asHexStringWithBase(toEncode):
	"""Converts a list of integers used as 8 bit values
	to a hexadecimal string with uppercase characters
	with the '0x' base indicator prepended; also works
	on bytes objects"""
	return (''.join(('0x%02X ' % x) for x in toEncode)).rstrip()

def hexStringToBytes(toDecode):
	"""Converts a hexadecimal string formatted like the
	output of asHexString to a bytes object"""
	return bytes(int('0x' + x, 16) for x in toDecode.split())

def chrsToString(toDecode):
	return ''.join(map(chr, toDecode))
