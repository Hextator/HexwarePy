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

import math

class Node():
	def __init__(self, key):
		self.key = key
		self.left = None
		self.right = None

	def __repr__(self):
		return str(self.key)

class ScapeGoatTree():
	def __init__(self, a):
		self.alpha = a
		self.size = 0
		self.maxSize = 0
		self.root = None

	def size(self, node):
		if node == None:
			return 0
		return 1 + self.size(node.left) + self.size(node.right)

	# height(tree) <= log_1/alpha(NodeCount)
	def heightLimit(self):
		return math.floor(math.log(self.size, 1.0/self.alpha))

	def heightExceeded(self, depth):
		return depth > self.heightLimit()

	def sibling(self, node, parent):
		if parent.left != None and parent.left.key == node.key:
			return parent.right
		return parent.left

	def rebalance(self, root, length):
		def sortedList(node, nodes):
			if node == None:
				return
			sortedList(node.left, nodes)
			nodes.append(node)
			sortedList(node.right, nodes)

		# Build a balanced binary tree for a sort list of nodes
		def balancedInsert(nodes, start, end):
			if start > end:
				return None
			mid = int(math.ceil(start + (end - start)/2.0))
			# Median node
			node = Node(nodes[mid].key)
			node.left = balancedInsert(nodes, start, mid - 1)
			node.right = balancedInsert(nodes, mid + 1, end)
			return node

		nodes = []
		sortedList(root, nodes)
		return balancedInsert(nodes, 0, length - 1)

	def minimum(self, node):
		while node.left != None:
			node = node.left
		return node

	def delete(self, toDelete):
		node = self.root
		parent = None
		isLeftChild = True
		while node.key != toDelete:
			parent = node
			if toDelete > node.key:
				node = node.right
				isLeftChild = False
			else:
				node = node.left
				isLeftChild = True

		successor = None
		# Case 1: Node to be deleted has no children
		if node.left == None and node.right == None:
			pass
		# Case 2: Node has only a right child
		elif node.left == None:
			successor = node.right
		# Case 3: Node has only a left child
		elif node.right == None:
			successor = node.left
		# Case 4: Node has a left and a right child
		else:
			# Find successor
			successor = self.minimum(node.right)
			# If the successor is the node's right child
			if successor == node.right:
				successor.left = node.left
			else:
				successor.left = node.left
				temp = successor.right
				successor.right = node.right
				node.right.left = temp

		# Replace the node
		if parent == None:
			self.root = successor
		elif isLeftChild:
			parent.left = successor
		else:
			parent.right = successor

		self.size -= 1
		if self.size < self.alpha * self.maxSize:
			self.root = self.rebalance(self.root, self.size)
			self.maxSize = self.size

	def search(self, key):
		curr = self.root
		while curr != None:
			if curr.key > key:
				curr = curr.left
			elif curr.key < key:
				curr = curr.right
			else:
				return curr;
		return None

	def insert(self, key):
		newNode = Node(key)
		parent = None
		currpar = self.root
		depth = 0
		parents = []
		while currpar != None:
			# Prepend
			parents.insert(0, currpar)
			parent = currpar
			if newNode.key < currpar.key:
				currpar = currpar.left
			else:
				currpar = currpar.right
			depth += 1

		if parent == None:
			self.root = newNode
		elif newNode.key < parent.key:
			parent.left = newNode
		else:
			parent.right = newNode

		self.size += 1
		self.maxSize = max(self.size, self.maxSize)
		
		if self.heightExceeded(depth):
			scapegoat = None
			parents.insert(0, newNode)
			sizes = [0] * len(parents)
			idx = 0
			# Find the highest scapegoat on the tree
			for i in range(1, len(parents)):
				sizes[i] = sizes[i - 1] + self.size(self.sibling(parents[i - 1], parents[i])) + 1
				if not self.isAlphaWeightBalanced(parents[i], sizes[i] + 1):
					scapegoat = parents[i]
					idx = i
			
			temp = self.rebalance(scapegoat, sizes[idx] + 1)
			
			scapegoat.left = temp.left
			scapegoat.right = temp.right
			scapegoat.key = temp.key

	def isAlphaWeightBalanced(self, node, sizeOfNode):
		a = self.size(node.left) <= (self.alpha * sizeOfNode)
		b = self.size(node.right) <= (self.alpha * sizeOfNode)
		return a and b

	def preOrder(self, node, inlist):
		if node != None:
			inlist.append(node.key)
			self.preOrder(node.left, inlist)
			self.preOrder(node.right, inlist)
		return inlist

	def inOrder(self, node, inlist):
		if node != None:
			self.inOrder(node.left, inlist)
			inlist.append(node.key)
			self.inOrder(node.right, inlist)
		return inlist

	def postOrder(self, node, inlist):
		if node != None:
			self.postOrder(node.left, inlist)
			self.postOrder(node.right, inlist)
			inlist.append(node.key)
		return inlist

	def __repr__(self):
		return str(self.inOrder(self.root, []))
