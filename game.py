from helpers import wrap

class Game:
	"""The Game class represents the world. Internally, we use a
	graph of Location objects and Item objects, which can be at a 
	Location or in the player's inventory. Each location has a set of
	exits which are the directions that a player can move to get to an
	adjacent location. The player can move from one location to another
	by typing a command like "Go North".
	"""
	def __init__(self, start):
		# start is the location in the game where the player starts
		self.curloc = start
		self.curloc.has_been_visited = True
		# inventory is the set of objects that the player has collected
		# could be updated with a Player object that holds this
		self.inventory = {}
		self.dialogue = {}
		# Print the special commands associated with items in the game
		# (helpful for debugging issues)
		self.print_commands = False

	def add_dialogue(self, name, dialogue, preconditions={}):
		"""dialogue is a Dialogue object, preconditions is the set of preconditions
		required to trigger the dialogue."""
		self.dialogue[name] = (dialogue, preconditions)

	def describe(self):
		"""Describe the current game state by first describing the
		location, then listing any exits, and then describing the items
		in the current location"""
		print("\n{0}".format(self.curloc.name.upper()))
		self.describe_current_location()
		self.describe_exits()
		self.describe_items()

	def describe_current_location(self):
		"""Describe the current location by printing its description field."""
		wrap(self.curloc.description)

	def describe_exits(self):
		"""List the directions that the player can take to exit from
		the current location"""
		exits = []
		for exit in self.curloc.connections.keys():
			exits.append(exit.upper())
		if len(exits) > 0:
			print("You can go: ", end = '')
			print(*exits, sep=", ")

	def describe_items(self):
		"""Describe what (visible) objects are in the room."""
		if len(self.curloc.items) > 0:
			print("You see: ")
			for name in self.curloc.items:
				item = self.curloc.items[name]
				print("  {0}".format(item.description))
				if self.print_commands:
					special_commands = item.get_commands()
					for cmd in special_commands:
						print('\t', cmd)

	def add_to_inventory(self, item):
		"""Add an item to the player's inventory."""
		self.inventory[item.name] = item

	def has_item(self, item_name):
		return item_name in self.inventory

	def get_from_inventory(self, item_name):
		return self.inventory.pop(item_name, None)

	def get_items_in_scope(self):
		"""Returns a list of items in the current location and in the inventory"""
		items_in_scope = []
		for name in self.curloc.items:
			items_in_scope.append(self.curloc.items[name])
		for name in self.inventory:
			items_in_scope.append(self.inventory[name])
		return items_in_scope