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

# Provides functions for interacting with arrays of raw data

def get16FromIntList(intlist, ind, big = False):
	"""Pulls 2 bytes from a list of integers treated as 8 bit values
	at the given index and converts them as if they formed an aligned
	16 bit (little endian by default) value (regardless of actual alignment)"""
	bottom = intlist[ind]
	top = intlist[ind + 1]
	if big:
		return ((bottom << 8) | (top & 0xFF)) & 0xFFFF
	return ((top << 8) | (bottom & 0xFF)) & 0xFFFF

def put16ToIntList(intlist, value, ind, big = False):
	"""Puts 2 bytes into a list of integers treated as 8 bit values
	at the given index and converts them as if they formed an aligned
	16 bit (little endian by default) value (regardless of actual alignment)"""
	bottom = value & 0xFF
	top = (value & 0xFF00) >> 8
	if big:
		intlist[ind] = top
		intlist[ind + 1] = bottom
	else:
		intlist[ind] = bottom
		intlist[ind + 1] = top

def get32FromIntList(intlist, ind, big = False):
	"""Pulls 4 bytes from a list of integers treated as 8 bit values
	at the given index and converts them as if they formed an aligned
	32 bit (little endian by default) value (regardless of actual alignment)"""
	byte1 = intlist[ind]
	byte2 = intlist[ind + 1]
	byte3 = intlist[ind + 2]
	byte4 = intlist[ind + 3]
	if big:
		return (((byte1 & 0xFF) << 24) | ((byte2 & 0xFF) << 16) | \
			((byte3 & 0xFF) << 8) | (byte4 & 0xFF)) & 0xFFFFFFFF
	return (((byte4 & 0xFF) << 24) | ((byte3 & 0xFF) << 16) | \
		((byte2 & 0xFF) << 8) | (byte1 & 0xFF)) & 0xFFFFFFFF

def put32ToIntList(intlist, value, ind, big = False):
	"""Puts 4 bytes into a list of integers treated as 8 bit values
	at the given index and converts them as if they formed an aligned
	32 bit (little endian by default) value (regardless of actual alignment)"""
	byte1 = value & 0xFF
	byte2 = (value & 0xFF00) >> 8
	byte3 = (value & 0xFF0000) >> 16
	byte4 = (value & 0xFF000000) >> 24
	if big:
		intlist[ind] = byte4
		intlist[ind + 1] = byte3
		intlist[ind + 2] = byte2
		intlist[ind + 3] = byte1
	else:
		intlist[ind] = byte1
		intlist[ind + 1] = byte2
		intlist[ind + 2] = byte3
		intlist[ind + 3] = byte4

def get16FromString(instr, ind, big = False):
	"""Returns a 16 bit value (in little endian form by default)
	from a given string at the given index with
	alignment ignored"""
	bottom = ord(instr[ind])
	top = ord(instr[ind + 1])
	if big:
		return ((bottom << 8) | (top & 0xFF)) & 0xFFFF
	return ((top << 8) | (bottom & 0xFF)) & 0xFFFF

def get32FromString(instr, ind, big = False):
	"""Returns a 32 bit value (in little endian form by default)
	from a given string at the given index with
	alignment ignored"""
	byte1 = ord(instr[ind])
	byte2 = ord(instr[ind + 1])
	byte3 = ord(instr[ind + 2])
	byte4 = ord(instr[ind + 3])
	if big:
		return (((byte1 & 0xFF) << 24) | ((byte2 & 0xFF) << 16) | \
		((byte3 & 0xFF) << 8) | (byte4 & 0xFF)) & 0xFFFFFFFF
	return (((byte4 & 0xFF) << 24) | ((byte3 & 0xFF) << 16) | \
		((byte2 & 0xFF) << 8) | (byte1 & 0xFF)) & 0xFFFFFFFF

def put16ToTuple(num, big = False):
	"""Returns a tuple of the (little endian by default)
	bytes of a given 16 bit integer"""
	top = (num >> 8) & 0xFF
	bottom = num & 0xFF
	if big:
		return (top, bottom)
	return (bottom, top)

def put32ToTuple(num, big = False):
	"""Returns a tuple of the (little endian by default)
	bytes of a given 32 bit integer"""
	byte4 = (num >> 24) & 0xFF
	byte3 = (num >> 16) & 0xFF
	byte2 = (num >> 8) & 0xFF
	byte1 = num & 0xFF
	if big:
		return (byte4, byte3, byte2, byte1)
	return (byte1, byte2, byte3, byte4)


def getStringFromIntList(intlist, ind, length = None, expectedEncoding = 'ASCII'):
	"""Pulls a string from a list of integers, treated as ASCII and null terminated by default,
	from the given index, with the length and encoding optionally able to be specified"""
	if 0 == length:
		return ''
	index = -1
	data = []
	while True:
		index += 1
		if length and length <= index:
			break
		value = intlist[ind + index]
		if not length and not value:
			break
		data.append(value)
	return bytes(data).decode(encoding = expectedEncoding)
