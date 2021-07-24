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

# This module provides the decorators "@Virtual" and "@Interface"
# which control the prevention and causation of cast exceptions
# enforced by rules similar to those of interfaces from other languages

import inspect

def getArgSpec(func):
	out = None
	try:
		out = inspect.getargspec(func)
	except: pass
	return out

def getRequiredArgs(func):
	argSpec = getArgSpec(func)
	if argSpec == None:
		return None
	out = None
	defaults = 0
	out = argSpec.args
	if out != None:
		try:
			defaults = len(argSpec.defaults)
		except: pass
		if defaults > 0:
			out = out[0:-defaults]
	varargs = True if argSpec.varargs else False
	keywords = True if argSpec.keywords else False
	return (len(out), varargs, keywords)

class CastException(Exception):
	pass

def cast(inter, cls):
	return inter.__cast__(cls)

def Virtual(input):
	setattr(input, '__virtual__', True)
	return input

def Interface(cls):
	typeDict = { }
	typeName = cls
	while type(typeName) is not type:
		typeName = type(typeName)
	typeName = typeName.__name__
	new = dir(cls)
	for curr in dir(type('object', (object,), { })):
		new.remove(curr)
	for curr in new:
		currattr = getattr(cls, curr)
		argspec = getRequiredArgs(currattr)
		typeDict[curr] = (type(currattr), argspec)
		try:
			if getattr(currattr, '__virtual__'):
				delattr(cls, curr)
		except: pass
	def castFunc(thing):
		cls = thing
		while type(cls) is not type:
			cls = type(cls)
		name = cls.__name__
		for curr in list(typeDict):
			try:
				checkattr = getattr(cls, curr)
			except AttributeError as ex:
				raise CastException(str(ex))
			checkattrtype = type(checkattr)
			expectedtype = typeDict[curr][0]
			#print(checkattrtype, '\n', expectedtype, sep='')
			if checkattrtype != expectedtype:
				raise CastException(' Could not cast to type \'' + typeName + '\': attribute \'' + curr + '\' is not of correct type in type \'' + name + '\'')
			argcheck = typeDict[curr][1]
			reqs = getRequiredArgs(checkattr)
			#print(argcheck, '\n', reqs, sep='')
			if argcheck != None and argcheck != reqs:
				raise CastException('Method \'' + curr + '\' does not have the correct argument specification to comply with type \'' + typeName + '\' in type \'' + name + '\'')
	outtype = type(cls.__name__ + '_inter', (cls,), { })
	setattr(outtype, '__cast__', castFunc)
	return outtype
