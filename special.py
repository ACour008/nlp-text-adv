def add_item_to_inventory(game, *args):
	""" Add a newly created Item and add it to your inventory. """
	(item, action_description, already_done_description) = args[0]
	if not game.is_in_inventory(item):
		print(action_description)
		game.add_to_inventory(item)
	else:
		print(already_done_description)
	return False

def describe_something(game, *args):
	""" Describe some aspect of the Item. """
	(description) = args[0]
	print(description)
	return False

def destroy_item(game, *args):
	""" Removes an Item from the game by setting its location is set to None. """
	(item, action_description, already_done_description) = args[0]
	if game.is_in_inventory(item):
		game.inventory.pop(item.name)
		print(action_description)
	elif item.name in game.curloc.items:
		game.curloc.remove_item(item)
		print(action_description)
	else:
		print(already_done_description)
	return False

def create_item(game, *args):
	(item, action_description, already_done_description) = args[0]
	if not game.curloc.has_item(item):
		game.curloc.add_item(item.name, item)
		print(action_description)
	else:
		print(already_done_description)
	return False

def end_game(game, *args):
	"""Ends the game."""
	end_message = args[0]
	print(end_message)
	return True

def move_to_room(game, *args):
	room, fail_message = args[0]
	game.curloc = room
	game.describe()
	return False

def toggle_room_condition(game, *args):
	condition_name, description_after_true, description_after_false = args[0]
	game.curloc.toggle_condition(condition_name)
	if game.curloc.conditions[condition_name] == True:
		print(description_after_true)
	else:
		print(description_after_false)
	return False

def remove_room_block(game, *args):
	direction, action_description, already_done_description = args[0]
	if game.curloc.remove_block(direction):
		print(action_description)
	else:
		print(already_done_description)
	return False

def perform_multiple_actions(game, *args):
	"""Allows you to perform multiple actions."""
	actions = args[0]
	for action in actions:
		action[0](game, action[1])
