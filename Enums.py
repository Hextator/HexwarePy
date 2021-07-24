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

# This module provides functions for creating an entity of a new type "enum",
# which can be used similarly to enum types from other languages,
# and interfacing with that type

# Example usage:
# >>> import Enums
# >>> currEnum = Enums.enum('test', 'me', out = 3)
# >>> len(currEnum)
# 3
# >>> currEnum.test
# 0
# >>> currEnum.me
# 1
# >>> currEnum.out
# 3
# >>> Enums.listEnumLabels(currEnum)
# ['test', 'me', 'out']

def listEnumLabels(enumIn):
	return enumIn.__enumlabels__

def lookup(enumIn, index):
	return enumIn.__lookupmap__[index]

def getItem(enumIn, key):
	return getattr(enumIn, key)

def hasItem(enumIn, key):
	return hasattr(enumIn, key)

def enum(*sequential, **named):
	enums = dict(zip(map(lambda x: x.replace(' ', ''), sequential), range(len(sequential))), **named)
	valsToKeys = {}
	for key in enums:
		value = enums[key]
		valsToKeys[value] = key
	def lenFunc(self):
		return len(enums) - 7
	enums['__len__'] = lenFunc
	enums['__contains__'] = hasItem
	enums['__getitem__'] = getItem
	enums['__enumlabels__'] = list(sequential) + list(named)
	enums['__lookupmap__'] = valsToKeys
	enums['listEnumLabels'] = listEnumLabels
	enums['lookup'] = lookup
	return type('Enum', (), enums)()
