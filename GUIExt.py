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

# Provides functions for managing a simple GUI

import tkinter

import Enums

__tkinter_root__ = None
def usingGUI():
	return __tkinter_root__ != None
def quitGUI():
	global __tkinter_root__
	if usingGUI():
		__tkinter_root__.quit()
def initGUI():
	global __tkinter_root__
	quitGUI()
	__tkinter_root__ = tkinter.Tk()
def supportDialogs():
	global __tkinter_root__
	initGUI()
	__tkinter_root__.withdraw()
def __ensure_tkinter__():
	global __tkinter_root__
	if not usingGUI():
		supportDialogs()
def getRoot():
	__ensure_tkinter__()
	return __tkinter_root__

DialogTypes = Enums.enum('OpenFile', 'OpenFiles', 'SaveAsFile', 'SaveAsFiles', 'ChooseDir')

def fileHelper(diagType, desc):
	__ensure_tkinter__()
	filedialog = __import__('tkinter.filedialog').filedialog
	toCall = filedialog.askopenfilename
	msg = 'Select '
	if DialogTypes.SaveAsFile == diagType:
		toCall = filedialog.asksaveasfilename
		msg += 'where to save ' + desc
	elif DialogTypes.ChooseDir == diagType:
		toCall = filediaog.askdirectory
		msg += 'folder to use for ' + desc
	else:
		msg += desc + ' for opening'
	result = toCall(title = msg)
	return result if result else None

def openPath(desc):
	return fileHelper(DialogTypes.OpenFile, desc)

def savePath(desc):
	return fileHelper(DialogTypes.SaveAsFile, desc)

def chooseDir(desc):
	return fileHelper(DialogTypes.ChooseDir, desc)
