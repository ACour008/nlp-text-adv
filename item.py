from preconditions import check_preconditions

class Item:
	"""Items are any objects that a player can get, or otherwise
	examine."""

	def __init__(self,
				 name,
				 description,
				 examine_text="",
				 take_text="",
				 start_at=None,
				 gettable=True,
				 take_fail = "",
				 use_data = None,
				 use_fail = "",
				 end_game=False):
		# The name of the object
		self.name = name
		# The default description of the object
		self.description = description
		# The detailed description when the player examines the object
		self.examine_text = examine_text
		# Text that displays when player takes an object
		self.take_text = take_text if take_text else ("You take the %s." % self.name)
		# Indicates whether a player can get the object and put it in their inventory
		self.gettable = gettable
		# Text that displays when gettable is false
		self.take_fail = take_fail if take_fail else ("You can't take the %s." % self.name)
		# Text that displays when use command fails
		self.use_fail = use_fail if use_fail else ("How do you want to use the %s?" % self.name)
		# True if entering this location should end the game.
		self.end_game = end_game
		# All the commands that the item responds to
		self.commands = {}
		# Certain conditions that track the item's state
		self.conditions = {}
		# All items that this item can interact with
		self.interacts_with = {}
		# The location in the Game where the object starts.
		if start_at:
			start_at.add_item(name, self)
		if use_data:
			# Should be (function, args, preconditions)
			self.commands['use'] = use_data

	def get_commands(self):
		"""Returns a list of special commands associated with this object."""
		return self.commands.keys()

	def add_interaction(self, item, function, args, preconditions={}):
		self.interacts_with[item.name] = (function, args, preconditions)
		if not item.has_interaction(self.name):
			item.add_interaction(self, function, args, preconditions)

	def add_interactions(self, itemset_list):
		for itemset in itemset_list:
			item, function, args, preconditions = itemset
			item.add_interaction(item, function, args, preconditions)

	def has_interaction(self, name):
		return name in self.interacts_with

	def do_interaction(self, game, items_list=None):
		"""Perform actions based on whether "use" command was called with one object
		or two or more. If one, it sees if there is a use command. If more than one,
		it checks if the two items can be used together or not."""
		end_game = False
		if items_list:
			for item_name in items_list:
				for name in self.interacts_with:
					if item_name == name:
						function, args, preconditions = self.interacts_with[name]
						if check_preconditions(preconditions, game, True):
							end_game = function(game, args)
		else:
			#Carry out the thing its suppose to do.
			if "use" in self.commands:
				print("Carrying out use command")
			else:
				print(self.use_fail)
		return end_game

	def add_action(self, command_text, function, args, preconditions={}):
		"""Add a special action associated with this item.
		function is what tha game will carry out when the player inputs the command_text
		the args is the arguments that are needed for the function.
		preconditions are what is needed before the function is fired.
		"""
		self.commands[command_text] = (function, args, preconditions)

	def do_action(self, command_text, game):
		"""Perform a special action associated with this item"""
		end_game = False # Switches to True if this action ends the game
		if command_text in self.commands:
			function, args, preconditions = self.commands[command_text]
			if check_preconditions(preconditions, game):
				end_game = function(game, args)
		else:
			print("You can't do that here.")
		return end_game