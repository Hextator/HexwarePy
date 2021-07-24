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

def QSpartition(inlist, left, right, pivIdx, compare = None):
	pivot = inlist[pivIdx]
	inlist[pivIdx] = inlist[right]
	inlist[right] = pivot
	storeIdx = left
	if not compare:
		compare = lambda x, y: x < y
	for i in range(left, right):
		#if inlist[i] <= pivot:
		if not compare(pivot, inlist[i]):
			temp = inlist[storeIdx]
			inlist[storeIdx] = inlist[i]
			inlist[i] = temp
			storeIdx = storeIdx + 1
	temp = inlist[storeIdx]
	inlist[storeIdx] = inlist[right]
	inlist[right] = temp
	return storeIdx

def inPlaceQuicksort(inlist, left, right, compare = None):
	if left < right:
		pivIdx = left + int((right - left)/2)
		newPivIdx = QSpartition(inlist, left, right, pivIdx, compare)
		inPlaceQuicksort(inlist, left, newPivIdx - 1, compare)
		inPlaceQuicksort(inlist, newPivIdx + 1, right, compare)

def quicksort(inlist, compare = None):
	if inlist is None or not inlist:
		return []
	inlen = len(inlist)
	if inlen == 1:
		return inlist
	pivIdx = int(inlen/2)
	pivot = inlist[pivIdx]
	inlist[pivIdx] = inlist[0]
	inlist[0] = pivot
	if not compare:
		compare = lambda x, y: x < y
	                                         #if x < pivot
	lesser = quicksort([x for x in inlist[1:] if compare(x, pivot)], compare)
	                                          #if x >= pivot
	greater = quicksort([x for x in inlist[1:] if not compare(x, pivot)], compare)
	return lesser + [pivot] + greater
