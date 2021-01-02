from location import Location
from item import Item
from game import Game
from parser import Parser
from preconditions import check_preconditions
from special import add_item_to_inventory, describe_something, destroy_item, end_game

def build_game():
	# Locations
	cottage = Location("Cottage", "You are standing in a small cottage.")
	garden_path = Location("Garden Path", "You are standing on a lush garden path. There is a cottage here.")
	cliff = Location("Cliff", "There is a steep cliff here. You call off the cliff and lose the game. THE END", end_game=True)
	fishing_pond = Location("Fishing Pond", "You are at the edge of a small fishing pond.")

	# Connections
	cottage.add_connection("out", garden_path)
	garden_path.add_connection("west", cliff)
	garden_path.add_connection("south", fishing_pond)

	# Items that you can pick up
	fishing_pole = Item("pole", "a fishing pole", "A SIMPLE FISHING POLE.", start_at=cottage)
	potion = Item("potion", "a poisonous potion", "IT'S A BRIGHT GREEN AND STEAMING.", start_at=cottage, take_text="As you near the potion, the fumes cause you to faint and lose the game. THE END", end_game=True)
	rosebush = Item("rosebush", "a rosebush", "THE ROSEBUSH CONTAINS A SINGLE RED ROSE. IT IS BEAUTIFUL.", start_at=garden_path)
	rose = Item("rose", "a red rose", "IT SMELLS GOOD.", start_at=None)
	fish = Item("fish", "a dead fish", "IT SMELLS TERRIBLE.", start_at=None)

	# Scenery (not things you can pick up)
	pond = Item("pond", "a small fishing pond", "THERE ARE FISH IN THE POND", start_at=fishing_pond, gettable=False)

	# Add special functions to your items
	rosebush.add_action("pick rose", add_item_to_inventory, (rose, "You pick the lone rose from the rosebush", "You already picked the rose."))
	rose.add_action("smell rose", describe_something, ("It smells sweet."))
	pond.add_action("catch fish", describe_something, ("You reach into the pond and try to catch a fish with your hands, but they are too fast."))
	pond.add_action("catch fish with pole", add_item_to_inventory, (fish, "You dip your hook into the pond and catch a fish. Nice moves!", "As much as you tried, you can't catch another fish"), preconditions={"inventory_contains":fishing_pole})
	fish.add_action("eat fish", end_game, ("Its definitely not sashimi grade, but you try to eat it anyway. It wasn't that bad. Either way, it was what you needed to win the game. Good job! THE END."))

	return Game(cottage)

def game_loop():
	game = build_game()
	parser = Parser(game)
	game.describe()

	command = ""
	while not (command.lower() == "exit" or command.lower == 'q'):
		command = input(">")
		end_game = parser.parse_command(command)
		if end_game:
			return
	#game_loop()
	print("THE GAME HAS ENDED.")

if __name__ == '__main__':
	game_loop()
