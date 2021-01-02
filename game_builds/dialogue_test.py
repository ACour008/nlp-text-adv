from location import Location
from item import Item
from npc import NPC
from dialogue import Dialogue, Node
from game import Game
from parser import Parser
from preconditions import check_preconditions
from special import add_item_to_inventory, describe_something, destroy_item, end_game, perform_multiple_actions, create_item

def build_game():
	room = Location("A room", "You are in a typical room in a rather generic building of some kind.")

	dog = Item("A dog", "A dog", "The dog is pretty quiet but looks like he could chat up a storm if engaged.",
			start_at=room, gettable=False)

	dialogue = Dialogue()
	start = Node("start", "DOG: You don't look like you're from here.", entry=True)
	bowler = Node("bowler", "DOG: Oh really, Then you must know Mr. Bowler.")
	newton = Node("newton", "DOG:Newton, eh? I heard there's trouble brewing down there.")
	liar = Node("liar", "DOG: You liar! There ain't no Mr. Bowler, I made him up!")
	starving = Node("starving", "DOG: Don't worry about it. Say, do you have something to eat? I'm starving.")

	dialogue.add_nodes(start, bowler, newton, liar, starving)
	
	start_lie = ("I've lived here my whole life!", 'start', 'bowler')
	start_true = ("I came here from Newton.", 'start', 'newton')
	friend_lie = ("Mr. Bowler is a good friend of mine!", 'bowler', 'liar')
	friend_true = ("Who?", 'bowler', 'starving')
	newton_lie = ("Did I saw Newton? I meant to say I am from here in Springtown.", "newton", "bowler")
	newton_true = ("I haven't heard of any trouble.", "newton", "starving")

	dialogue.add_edges(start_lie, start_true, friend_lie, friend_true, newton_lie, newton_true)

	game = Game(room)
	game.add_dialogue("dog", dialogue, preconditions={"location_has_item": dog})

	return game

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