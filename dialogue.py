class Dialogue:
	""" This is a directed graph. Or at least trying to be.
	Each set of dialogue is its own graph. You must create the nodes and edges
	using the appropriate functions when building the game.
	"""
	def __init__(self, data=None):
		if not data:
			self.data = {}
		self.start_node = None
		self.current_node = None
	
	def add_node(self, node):
		self.data[node.name] = node
		if node.entry:
			self.start_node = node
			self.current_node = node

	def add_nodes(self, *nodes):
		for node in nodes:
			self.add_node(node)

	def add_edge(self, response_text, from_node, to_node):
		edge = Edge(response_text, self.data[to_node])
		self.data[from_node].edges.append(edge)

	def add_edges(self, *edges):
		for edge in edges:
			(response_text, from_node, to_node) = edge
			self.add_edge(response_text, from_node, to_node)

	def start(self):
		print(self.current_node.text)
		if self.current_node.edges:
			for i, edge in enumerate(self.current_node.edges, 1):
				print("{0}: {1}".format(i, edge.text))
			print("{0}: Leave.".format(i+1))
			response = ""
			while not (response == str(i+1)) :
				response = input("[Enter a numbered response] >> ")
				end_dialogue = self.check_response(response)
				if end_dialogue:
					self.current_node = self.start_node
					return

	def check_response(self, response):
		end = False
		try:
			i = int(response) - 1
			if (i+1 == len(self.current_node.edges)+1):
				end = True
			elif i >= 0 and i <= len(self.current_node.edges):
				edge = self.current_node.edges[i]
				print("YOU: {0}".format(edge.text))
				if edge.next_node:
					self.current_node = edge.next_node
					print(self.current_node.text)
					if self.current_node.edges:
						for i, edge in enumerate(self.current_node.edges, 1):
							print("{0}: {1}".format(i, edge.text))
					else:
						end = True
			else:
				print("You try to say something completely out of context. It isn't well received... Want to try that again?")
		except:
			print("You utter some completely random jibberish and get a weird look for it. Want to try that again?")
		return end
				
class Node:
	"""Contains NPC Dialogue."""
	def __init__(self, name, text, entry=False):
		self.name = name
		self.text = text
		self.entry = entry
		self.edges = []

class Edge:
	"""The direction that connects Nodes"""
	def __init__(self, text, next_node=""):
		self.text = text
		self.next_node = next_node
