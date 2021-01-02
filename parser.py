import re
from string import punctuation
from random import randrange
from preconditions import check_preconditions
from helpers import wrap

class Parser():

	def __init__(self, game, lexicon):
		self.command_history = []
		self.game = game
		self.lexicon = lexicon

	def parse_command(self, command):
		self.command_history.append(command)
		end_game = False

		tokens = self.lexicon.tokenize(command) # Still need to split commands by ','
		command = self.check_structure(tokens) # Check if syntax is a proper command
		if command:
			# First word of command should match the command function below.
			action = getattr(self, command[0][0], None)
			if action:
				action(command)
			else:
				wrap("You can't {0}.".format(self.command_history[-1]))
		else:
			responses = ["Huh?", "What?", "Say again?", "Come again?",
				"Can you say that differently?", "Does. Not. Compute."]
			i = randrange(len(responses))
			wrap(responses[i])

	def check_structure(self, tokens):
		""" Checks to see if command syntax and structure is within the allowable synatax.
		If it is, it will return the tokens as is, if not, it will return a None object.
		The allowable syntax/structure is defined in the Lexicon object."""
		current = tuple(token[1] for token in tokens)
		if current in self.lexicon.allowed:
			return tokens
		return None


	### Parser Commands ###

	def attack(self, command_list):
		# A TODO
		pass

	def consume(self, command_list):
		pass

	def drop(self, command_list):
		item_names = command_list[1::2]

		for item_name in item_names:
			item = self.game.get_from_inventory(item_name[0])
			if item:
				self.game.curloc.add_item(item_name[0], item)
				wrap("You drop the {0}.".format(item.name))
			else:
				wrap("The {0} isn't in your inventory.".format(item_name[0]))

	def examine(self, command_list):
		pass

	def give(self, command_list):
		pass

	def go(self, command_list):
		direction = command_list[1][0]
		if direction:
			if direction in self.game.curloc.connections:
				if self.game.curloc.is_blocked(direction, self.game):
					wrap(self.game.curloc.get_block_description(direction))
				else:
					print(self.game.curloc.connections[direction].name)
					self.game.curloc = self.game.curloc.connections[direction]
					if self.game.curloc.end_game:
						self.game.describe_current_location()
					else:
						self.game.describe()
			else:
				print("You can't go %s from here." % direction.upper())
		return self.game.curloc.end_game

	def look(self, command_list):
		if len(command_list) == 1:
			self.game.describe()
		else:
			self.examine(command_list)

	def search(self, command_list):
		pass

	def take(self, command_list):
		end_game = False
		item_names = command_list[1::2]
		
		for item_name in item_names:
			# check to see if already in inventory
			if self.game.has_item(item_name[0]):
				wrap("You already have the {0}.".format(item_name[0]))
			else:
				item = self.game.curloc.get_item(item_name[0])
				if item:
					if item.gettable:
						matched_item = True
						self.game.add_to_inventory(item)
						wrap(item.take_text)
					else:
						print(item.take_fail)
				else:
					print("The {0} isn't here.".format(item_name[0]))

	def talk(self, command_list):
		pass

	def use(self, command_list):
		"""looks at the length of the sentence to see if player wants to use
		multiple items."""
		if len(command_list) == 1:
			print("What do you want to use?")
			
		elif len(command_list) == 2:
			# "use [item]" command
			item = self.game.get_item(command_list[1][0])
			if item:
				item.do_interaction(self.game)
			else:
				print("You can't use that.")

		elif (len(command_list) > 2 and len(command_list) % 2 == 0):
			# "use [item] with/and [item]..." command
			item = self.game.get_item(command_list[1][0])
			if item:
				other_items = [cmd[0] for cmd in command_list[3::2]] # every second item after 4th word
				print(other_items)
				item.do_interaction(self.game, other_items)

		elif len(command_list) % 2 == 1:
			# incomplete command
			print("You want to use what with what?")

		else:
			print("What do you want to use?")