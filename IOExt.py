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

# Provides additional functions for managing application and user
# input and output

import sys
import inspect

import os
import shutil

import hashlib

import re

import TextExt

# XXX: This function didn't work anymore and now it has tacky platform specific stuff in it
def ensureDir(path):
	if os.path.isdir(path):
		return
	try:
		os.makedirs(path)
	except OSError as ose:
		try:
			if ose.errno != errno.EEXIST:
				raise
		except NameError: pass
	except Exception as e:
		try:
			if type(e) is WindowsError:
				if 17 != e.errno:
					raise
		except: pass

def clearEmptyDirs(currDir, removeRoot = True):
	if not os.path.isdir(currDir):
		return

	paths = os.listdir(currDir)
	for path in paths:
		fullPath = os.path.join(currDir, path)
		if os.path.isdir(fullPath):
			clearEmptyDirs(fullPath)

	paths = os.listdir(currDir)
	if removeRoot and not paths:
		try:
			os.rmdir(currDir)
		except: pass

def copyFile(sourcePath, targetPath):
	if os.path.exists(targetPath):
		raise OSError(targetPath + ' already exists')
	ensureDir(os.path.dirname(targetPath))
	shutil.copyfile(sourcePath, targetPath)

def copyFileSilentFail(sourcePath, targetPath):
	try:
		copyFile(sourcePath, targetPath)
	except: pass

def deleteDirectory(dirPath):
	if os.path.isdir(dirPath):
		shutil.rmtree(dirPath)
	else:
		raise OSError(dirPath + ' is not a directory')

def deleteDirectorySilentFail(dirPath):
	try:
		deleteDirectory(dirPath)
	except: pass

def deleteFile(filePath):
	os.remove(filePath)

def deleteFileSilentFail(filePath):
	try:
		deleteFile(filePath)
	except: pass

def overwriteFile(sourcePath, targetPath):
	ensureDir(os.path.dirname(targetPath))
	shutil.copyfile(sourcePath, targetPath)

def overwriteFileSilentFail(sourcePath, targetPath):
	try:
		overwriteFile(sourcePath, targetPath)
	except: pass

def getHash(filePath):
	data = None
	with open(filePath, 'rb') as fileHandle:
		data = fileHandle.read()
	md5 = hashlib.md5()
	md5.update(data)
	return md5.digest()

def fileStats(filePath):
	fileSize = os.path.getsize(filePath)
	md5Hash = getHash(filePath)
	return (fileSize, md5Hash)

def dirStats(currFullPath, skipPatterns = [], skipInRoot = []):
	""""skipPatterns" should be a list of "re.Pattern" typed items
	which represent paths to ignore in any subdirectory or in the root;
	"skipInRoot" should be a list of strings of base file or
	directory names to only be skipped if they are in the root."""

	currFolders = 0
	currFiles = 0
	currBytes = 0
	if os.path.isdir(currFullPath):
		for path in os.listdir(currFullPath):
			fullSubPath = os.path.join(currFullPath, path).replace(os.sep, '/')
			patternMatch = False
			if skipPatterns:
				for pattern in skipPatterns:
					if pattern.search(fullSubPath):
						patternMatch = True
						break
			if patternMatch:
				continue
			if os.path.isdir(fullSubPath):
				if skipInRoot and path in skipInRoot:
					continue
				currFolders += 1
				subFolders, subFiles, subBytes = dirStats(fullSubPath, skipPatterns)
				currFolders += subFolders
				currFiles += subFiles
				currBytes += subBytes
			elif os.path.isfile(fullSubPath):
				currFiles += 1
				currBytes += os.stat(fullSubPath).st_size
	return currFolders, currFiles, currBytes

def dirDiff(dir1, dir2, skipPatterns1 = [], skipPatterns2 = []):
	""""skipPatterns1" applies to "dir1"; "skipPatterns2"
	applies to "dir2"; both should be lists of "re.Pattern"
	typed items."""

	dir1 = os.path.normpath(dir1)
	allDir1Files = [os.path.normpath(os.path.join(root, fileName)) for root, dirs, files in os.walk(dir1) for fileName in files]
	dir1Files = []
	if skipPatterns1:
		dir1Files = TextExt.filterByRegexList(allDir1Files, skipPatterns1, False)
	else:
		dir1Files = allDir1Files
	dir1Files = [os.path.relpath(file, start = dir1) for file in dir1Files]

	dir2 = os.path.normpath(dir2)
	allDir2Files = [os.path.normpath(os.path.join(root, fileName)) for root, dirs, files in os.walk(dir2) for fileName in files]
	dir2Files = []
	if skipPatterns2:
		dir2Files = TextExt.filterByRegexList(allDir2Files, skipPatterns2, False)
	else:
		dir2Files = allDir2Files
	dir2Files = [os.path.relpath(file, start = dir2) for file in dir2Files]

	in1Only = []
	inBothButDiff = []
	in2Only = []
	inBoth = []

	# UGH
	if 'nt' == os.name:
		dir1FilesLower = list(map(str.lower, dir1Files))
		dir2FilesLower = list(map(str.lower, dir2Files))
		in1Only = list([file for file in dir1Files if file.lower() not in dir2FilesLower])
		inBoth = list([file for file in dir1Files if file.lower() in dir2FilesLower])
		in2Only = list([file for file in dir2Files if file.lower() not in dir1FilesLower])
	else:
		in1Only = list([file for file in dir1Files if file not in dir2Files])
		inBoth = list([file for file in dir1Files if file in dir2Files])
		in2Only = list([file for file in dir2Files if file not in dir1Files])

	# TODO: Also make sure timestmaps of last modification match
	inBothButDiff = list([file for file in inBoth if os.path.getsize(os.path.join(dir1, file)) != os.path.getsize(os.path.join(dir2, file))])

	return in1Only, inBothButDiff, in2Only, inBoth

# Note: os.linesep (such as '\n') and os.sep (such as '/') are too simple to include here

def splitPathExt(path):
	outPath, extension = os.path.splitext(path)
	extension = extension.rstrip()
	return outPath, extension

def getClass(classString):
	"""Returns an object of a class based on a
	name specifying a path to the class relative
	to a directory in the include list(s)"""
	parts = classString.split('.')
	module = ".".join(parts[:-1])
	classObj = __import__(module)
	for comp in parts[1:]:
		classObj = getattr(classObj, comp)			
	return classObj

__location__ = ''
__location_init__ = False
def __init_loc__(arg = None, file = None):
	"""Ensures __location__ refers to the folder this script is in"""
	global __location__
	global __location_init__
	if __location_init__: return
	__location_init__ = True
	cwd = os.getcwd()
	if file:
		dirnameVar = file
	elif arg:
		dirnameVar = arg
		cwd = ''
	else:
		trace = inspect.stack()
		callingFile = trace[0][1]
		for frame in trace:
			if frame[1] == callingFile:
				continue
			callingFile = frame[1]
			break
		__location__ = os.path.dirname(callingFile)
		return
		# try:
			# __file__
			# dirnameVar = __file__
		# except NameError:
			# dirnameVar = sys.argv[0]
			# cwd = ''
	__location__ = os.path.realpath(os.path.join(cwd, os.path.dirname(dirnameVar)))
def getScriptLocation(arg = None, file = None):
	__init_loc__(arg, file)
	return __location__
def getResourceLocation(name, arg = None, file = None):
	return os.path.join(getScriptLocation(arg, file), name)
def getResource(name, mode = 'r', arg = None, file = None, encoding = None):
	"""Opens a file using a path relative to
	the directory this script is in;
	pass sys.argv[0] and __file__ as the latter two
	optional arguments to make it work for scripts
	which call these"""
	return open(getResourceLocation(name, arg, file), mode, encoding = encoding)
def putResource(name, mode = 'w', arg = None, file = None, encoding = None):
	return getResource(name, mode, arg, file, encoding = encoding)

__argIndex = 1
def initFromArgIndex(args, index, description, convert, fetch):
	global __argIndex
	__argIndex = index + 1
	if args and len(args) > index:
		string = args[index]
		if string is not None:
			return convert(string)
	return fetch(description)

def initFromArg(args, description, convert, fetch):
	return initFromArgIndex(args, __argIndex, description, convert, fetch)
