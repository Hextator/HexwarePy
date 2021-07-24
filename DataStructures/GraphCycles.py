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

# Graph node class

class gnode(object):
	def __repr__(self):
		return str(self.val)
	def __init__(self, v):
		self.val = v
		self.nodes = []

# Returns a list of the nodes in the graph as well as linking them to each other
# Input is expected to be in the form
#data0 = [[nodeCount, edgeCount], [startNode1, endNode1], etc]
#data1 = [[5, 5], [4, 1], [0, 3], [1, 2], [3, 1], [4, 2]]
#data2 = [[6, 9], [0, 1], [0, 5], [1, 2], [2, 5], [2, 4], [2, 3], [1, 3], [4, 5], [2, 4]]
# Run time is characterized by O(n) where n is the number of edges

def creategraph(inlist):
	meta = inlist[0]
	numVerts = meta[0]
	numEdges = meta[1]
	nodes = [gnode(x) for x in range(0, numVerts)]
	for edge in inlist[1:]:
		nodes[edge[0]].nodes.append(nodes[edge[1]])
		nodes[edge[1]].nodes.append(nodes[edge[0]])
	return nodes

# Finds all cycles of length "length" for a vertex recursively
# Finds them in all "directions", so there will be duplicates
# Output is like [[tri1NodeA, tri1NodeB, tri1NodeC], [tri2NodeA, ...], ...]
# where triXNodeY is a vertex in found triangle "X"
# Run time is characterized by O(d^length), where d is the number of child nodes

def findcycles(vertex, length):
	def cyclehelper(vertex, visited):
		if len(visited) == length:
			if visited[0].val == vertex.val:
				return [visited]
			else: return None
		newVisited = visited + [vertex]
		cycles = [[]]
		for child in vertex.nodes:
			if child not in newVisited or len(newVisited) == length:
				polygon = cyclehelper(child, [x for x in newVisited])
				if polygon and polygon != [[]]:
					cycles = cycles + polygon
		return cycles
	out = cyclehelper(vertex, [])
	return [x for x in out if x]

# Returns whether 2 given cycles are the "same" after ignoring direction
# Execution time is linear (O(n))

def samecycle(cyc1, cyc2):
	if not cyc1 or not cyc2: return False
	nodes1 = [x.val for x in cyc1]
	nodes2 = [x.val for x in cyc2]
	if len(nodes1) != len(nodes2): return False
	if len(nodes1) < 3:
		# Not a cycle
		return False
	for node in nodes1:
		if node not in nodes2:
			return False
	return True

# Concatenates and returns the lists returned by findcycles for each vertex
# in the graph represented by the given node list
# Run time is characterized by O(nd^length)
# where n is the number of nodes in the graph,
# d is the number of child nodes
# and length is 3

def alltris(nodelist):
	tris = [[]]
	for node in nodelist:
		tris = tris + findcycles(node, 3)
	return tris[1:]

# Iterates through the output of alltris for a graph and marks
# triangle duplicates found with sametri as empty node lists,
# then returns the list with the now empty node lists excluded
# Run time for duplicate removal is characterized by O(a^2)
# where n is the number of triangles (including duplicates) found by alltris
# Run time for alltris, characterized by O(nd^3), characterizes
# the run time of uniquetris due to being a greater order of magnitude
# of complexity than other operations within the function

def uniquetris(nodelist):
	tris = alltris(nodelist)
	for x in range(0, len(tris)):
		for y in range(0, len(tris)):
			if not tris[x] or not tris[y]: continue
			if x == y: continue
			if samecycle(tris[x], tris[y]):
				tris[y] = []
	return [x for x in tris if x]

# Solves and prints the unique triangles for the 2 given graphs

def solveGraphTriangles():
	data1 = [[5, 5], [4, 1], [0, 3], [1, 2], [3, 1], [4, 2]]
	graph1 = creategraph(data1)
	print(uniquetris(graph1))
	data2 = [[6, 9], [0, 1], [0, 5], [1, 2], [2, 5], [2, 4], [2, 3], [1, 3], [4, 5], [2, 4]]
	graph2 = creategraph(data2)
	print(uniquetris(graph2))
