from location import Location
from item import Item
from npc import NPC
from game import Game
from parser import Parser
from preconditions import check_preconditions
from special import add_item_to_inventory, describe_something, destroy_item, end_game, perform_multiple_actions, create_item

def build_game():
	#Locations
	bedroom = Location("Your bedroom", "Youre in your bedroom. Whatever.")
	kitchen = Location("Your kitchen", "You're in your kitchen. You've reached the end of the game!", end_game=True)

	#Items
	guard = Item("guard", "A guard blocking the door.", "HE LOOKS AT YOU SUSPICIOUSLY EVEN THOUGH THIS IS YOUR ROOM.",
		start_at=bedroom, gettable=False)
	unconcious_guard = Item("unconcious guard", "An unconcious guard is slumped up against the wall.",
		"HE LOOKS KNOCKED TF OUT", start_at=None, gettable=False)
	branch = Item("branch", "A branch on your floor", "DON'T LOOK AT ME, I DON'T KNOW HOW IT GOT THERE",
		start_at=bedroom, take_text="This looks like this could knock a mother fucker out if you hit them hard enough with it.")

	#Connections
	bedroom.set_connection("southwest", kitchen)

	#Blocks
	bedroom.add_block("southwest", "The guard is blocking your way", preconditions={"location_has_item": unconcious_guard})

	#Item Actions/Dialogue
	guard.add_action("hit guard with branch", perform_multiple_actions,
		([(destroy_item, (branch, "You swing the branch against the guard as hard as you can. The branch shatters to pieces",
			"You already tried that.")),
		(destroy_item, (guard, "The guard crumbles to the ground.", "")),
		(create_item, (unconcious_guard, "He looks knocked TF out.", ""))
		]), preconditions={"inventory_contains": branch, "location_has_item":guard})

	return Game(bedroom)


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