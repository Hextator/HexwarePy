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

import os
import sys
import re

import ConsoleExt
import IOExt

DEBUG = False

regex = re.compile('lib\\' + os.sep + 'site-packages')
pthName = 'python.pth'

def addToPath(where, cwd):
	where = os.path.join(where, pthName)
	ConsoleExt.debugPrint(DEBUG, 'where: ' + where)
	with open(where, 'a') as pathFile:
		pathFile.write(IOExt.getScriptLocation(cwd) + '\n')

def main(args):
	if len(args) > 1 and args[1] == 'install':
		notInPath = True
		ConsoleExt.debugPrint(DEBUG, 'pthName used: ' + pthName)
		# Iterate through sys paths
		for path in sys.path[1:]:
			ConsoleExt.debugPrint(DEBUG, 'sys.path: ' + path)
			if notInPath == False: break
			# Iterate through subfolders of sys paths
			for dirpath, dirnames, filenames in os.walk(path):
				if notInPath == False: break
				# Iterate through files in all folders and subfolders of sys paths
				for curr in filenames:
					if notInPath == False: break
					if pthName in curr:
						# Iterate through lines in those files
						with open(os.path.join(dirpath, curr), 'r') as pthFile:
							for line in pthFile:
								if IOExt.getScriptLocation(args[0]) in line:
									notInPath = False
									break
		if notInPath:
			ConsoleExt.debugPrint(DEBUG, 'Not in path')
			for path in sys.path:
				if regex.search(path):
					addToPath(path, args[0])
					break
		else:
			print('Was in path.')
			ConsoleExt.debugPrint(DEBUG, sys.path)

if __name__ == '__main__':
	if DEBUG: sys.argv[1] = 'install'
	main(sys.argv)
