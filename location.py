from preconditions import check_preconditions

class Location:
	"""Locations are the places in the game that a player can visit.
	Internally they are represented nodes in a graph. Each location stores
	a description of the location, any items in the location, its connections
	to adjacent locations, and any blocks that prevent movement to an adjacent
	location. The connections is a dictionary that its keys are directions
	and that its values are the location that the player can travel to. The
	travel_descriptions also have directions as keys, and its values are an
	optional short description of traveling to that location."""

	def __init__(self, name, description, end_game=False):
		# A short name for the locaiton
		self.name = name
		# A description of the location
		self.description = description
		# True is entering this location
		self.end_game = end_game
		# A dictionary mapping from directions to other Location objects
		self.connections = {}
		# A dictionary mapping from directions to text descriptions of the path there
		self.travel_descriptions = {}
		# A dictionary mapping from item name to Item objects present in this location
		self.items = {}
		# A dictionary mapping from direction to Block object in that direction
		self.blocks = {}
		# Flag that gets set to True once this location has been visited by the player
		self.has_been_visited = False
		# For any specific room commands - namely for startgame, endgame rooms.
		self.commands = {}
		# Conditions track room variables that may change.
		self.conditions = {}
		# Hints are help the player figure out puzzles/problems/
		self.hints = {'counter': 0, 'hints':[]}

	def add_connection(self, direction, connected_location, travel_description=""):
		"""Add a connection from the current location to a connected location.
		Direction is a string that the player can use to get to the connected
		location. If the direction is a cardinal direction, then we also
		automatically make a connection in the reverse direction."""
		self.connections[direction] = connected_location
		self.travel_descriptions[direction] = travel_description
		if direction == 'north':
			connected_location.connections['south'] = self
			connected_location.travel_descriptions['south'] = ""
		if direction == 'south':
			connected_location.connections['north'] = self
			connected_location.travel_descriptions['north'] = ""
		if direction == 'east':
			connected_location.connections['west'] = self
			connected_location.travel_descriptions['west'] = ""
		if direction == 'west':
			connected_location.connections['east'] = self
			connected_location.travel_descriptions['east'] = ""
		if direction == 'northeast':
			connected_location.connections['southwest'] = self
			connected_location.travel_descriptions['southwest'] = ""
		if direction == 'northwest':
			connected_location.connections['southeast'] = self
			connected_location.travel_descriptions['southeast'] = ""
		if direction == 'southeast':
			connected_location.connections['northwest'] = self
			connected_location.travel_descriptions['northwest'] = ""
		if direction == 'southwest':
			connected_location.connections['northeast'] = self
			connected_location.travel_descriptions['northeast'] = ""
		if direction == 'up':
			connected_location.connections['down'] = self
			connected_location.travel_descriptions['down'] = ""
		if direction == 'down':
			connected_location.connections['up'] = self
			connected_location.travel_descriptions['up'] = ""
		if direction == 'in':
			connected_location.connections['out'] = self
			connected_location.travel_descriptions['out'] = ""
		if direction == 'out':
			connected_location.connections['in'] = self
			connected_location.travel_descriptions['in'] = ""

	def add_action(self, command, function, args, preconditions={}):
		self.commands[command] = (function, args, preconditions)

	def get_commands(self):
		return self.commands.keys()

	def do_action(self, command_text, game):
		end_game = False
		if command_text in self.commands:
			function, args, preconditions = self.commands[command_text]
			if check_preconditions(preconditions, game):
				end_game = function(game, args)
		else:
			print("You can't do that here.")
		return end_game

	def has_item(self, item_name):
		return item_name in self.items
	
	def add_item(self, name, item):
		"""Put an item in this location."""
		self.items[name] = item

	def get_item(self, item):
		"""Remove an item from this location (i.e, if the player picks it up
		and stores it in their inventory)."""
		return self.items.pop(item, None)

	def is_blocked(self, direction, game):
		"""Checks if an obstacle is in the way of the direction."""
		if not direction in self.blocks:
			return False
		(block_description, preconditions) = self.blocks[direction]
		
		# print_failure_reasons off because the block is probably an Item object
		# that has its own built-in response. See already_done_description in
		# special functions.
		if check_preconditions(preconditions, game, print_failure_reasons=False):
			# All the preconditions have been met. You may pass.
			return False
		else:
			# There are still obstacles to overcome or puzzles to solve.
			return True

	def get_block_description(self, direction):
		"""Checks if there is an obstacle in this direction."""
		if not direction in self.blocks:
			return ""
		else:
			(block_description, preconditions) = self.blocks[direction]
			return block_description

	def add_block(self, blocked_direction, block_description, preconditions):
		"""Create an obstacle that prevents a player from going in a direction
		until all preconditions are met."""
		self.blocks[blocked_direction] = (block_description, preconditions)

	def remove_block(self, blocked_direction):
		return self.blocks.pop(blocked_direction, None)

	def set_condition(self, condition_name, value):
		self.conditions[condition_name] = value

	def toggle_condition(self, condition_name):
		self.conditions[condition_name] = not self.conditions[condition_name]
		