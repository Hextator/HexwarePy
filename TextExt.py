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

# Provides additional functions for reformatting and parsing text

import re

import ConsoleExt

DEBUG_COMMENTS = False
bcomm = re.compile(r'(\/\*|\*\/|\/\/|\\)')
def stripCPPstyleComments(file, supportBackslashExpressions = True, supportBlockComments = False):
	ignore = 0
	keep = False
	isComment = False
	for line in file:
		if len(line) > 0 and line[-1] == '\n':
			line = line[0:-1]
		if len(line) <= 0 or isComment:
			isComment = line.endswith('\\')
			continue
		if not keep:
			toAdd = ''
		keep = False
		tokens = bcomm.split(line)
		for token in tokens:
			if not token:
				continue
			if keep:
				keep = False
				if not supportBackslashExpressions:
					# C preprocessor would return here, but returning and breaking
					# both make data like "\\\\.\\COM2" unusable, which may be more
					# incorrect in certain contexts
					break
				else:
					# Instead this must be done
					toAdd += '\\'
			if ignore:
				if token == '*/':
					ignore -= 1
				elif token == '/*':
					if supportBlockComments:
						ignore += 1
			else:
				if token == '//':
					if line.endswith('\\'):
						isComment = True
					break
				elif token == '/*':
					ignore += 1
				elif token == '\\':
					keep = True
				else:
					toAdd += token
		#toAdd = toAdd.strip()
		if toAdd and not keep:
			ConsoleExt.debugPrint(DEBUG_COMMENTS, toAdd)
			yield toAdd

def stringToBytes(stringin):
	"""Converts a string object to a bytes object"""
	return stringin.encode('latin-1')

def bytesToString(bytesin):
	"""Converts a bytes object to a string object"""
	return bytesin.decode('latin-1')

def stringToIntList(string):
	"""Converts a list of strings to a list of integers
	if the string\'s characters can be converted"""
	return list(ord(x) for x in string)

def intListToString(msg):
	"""Converts a list of integers to a string, with
	input values masked to be less or equal to 255
	Also works on bytes objects"""
	return ''.join(chr(x & 0xFF) for x in msg)

def filterByRegexList(strings, expressions, keepMatches = True):
	output = []
	for currString in strings:
		patternMatch = False
		for pattern in expressions:
			if pattern.search(currString):
				patternMatch = True
				break
		patternMatch ^= keepMatches
		if not patternMatch:
			output.append(currString)
	return output
