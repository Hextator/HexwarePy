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

# Extension utilities for process management,
# such as wrapping subprocess calls or
# achieving mutually exclusive process execution

import os
import errno

import time

import IOExt

# From:
#	https://stackoverflow.com/questions/1444790/python-module-for-creating-pid-based-lockfile
#	https://stackoverflow.com/a/42967284
#	and
#	https://github.com/dmfrey/FileLock/blob/master/filelock/filelock.py
class FileLock:
	def __init__(self, lockPath = None, secondsToTimeOut = 0, delay = 1):
		# TOMAYBE: Is this a good default?
		defaultLockPath = os.path.join(os.path.expanduser('~'), 'Python.lock')
		self.lockPath = defaultLockPath if lockPath is None else lockPath
		self.lockFile = None
		self.locked = False
		self.timeOut = secondsToTimeOut
		self.reattemptDelay = delay

	def lock(self):
		lockTime = time.time()
		while True:
			try:
				# This opens the file for both writing AND reading,
				# will create it if it does not already exist,
				# and requires it to not exist already
				self.lockFile = os.open(self.lockPath, os.O_CREAT | os.O_EXCL | os.O_RDWR)
				self.locked = True
				break
			# TOMAYBE: This was IOError, but the doc says it's OSError now.
			# Is this accurate?
			except OSError as e:
				# If we get EEXIST, it just means we're still waiting on the lock,
				# but other errors are concerning
				if e.errno != errno.EEXIST:
					raise e
				else:
					time.sleep(self.reattemptDelay)
					if (time.time() - lockTime) >= self.timeOut:
						raise OSError('Failed to lock the file "' + self.lockPath + '".')

	def unlock(self):
		if self.locked and self.lockFile:
			# TOMAYBE: Can this fail?
			# What should be done if it can?
			# It would probably be best to just let the exception bubble up anyway
			os.close(self.lockFile)
			IOExt.deleteFile(self.lockPath)
			self.locked = False

	def __enter__(self):
		if not self.locked:
			self.lock()
		return self

	def __exit__(self, type, value, traceback):
		if self.locked:
			self.unlock()

	def __del__(self):
		self.unlock()

def fileLockWrapper(entryFunc, args, usageException, lockIndex = 1):
	"""Pops the "lockIndex" element from args, raising
	"usageException" if it can't, then runs "entryFunc(args)"
	with the modified "args" list if, and only if, the file
	path obtained by popping "args[lockIndex]" can be locked."""

	if lockIndex + 1 > len(args):
		raise usageException

	#lockPath = args[lockIndex]
	#args = [:lockIndex] + args[lockIndex + 1:]
	lockPath = args.pop(lockIndex)

	#lockObj = FileLock(lockPath)
	#lockObj.lock()
	#try:
	#	entryFunc(args)
	#finally:
	#	lockObj.unlock()

	with FileLock(lockPath) as lockObj:
		entryFunc(args)
