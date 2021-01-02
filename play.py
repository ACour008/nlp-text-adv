from game import Game
from location import Location
from item import Item
from parser import Parser
from lexicon.lexicon import Lexicon
import special as s


def builder():
	# rooms
	intro = Location("THIRTEEN MOON PROPHECY", "The year is 2051. Humankind narrowly avoided catestrophic destruction when a new energy source was developed by your parents 15 years ago. The discovery established the first possibilities of space travel through jump-gates. Few were quick to capitalize on the emerging market, including you and your family, making you and your family the first trillionaires in the galaxy. Welcome to the Thirteen Moon Prophecy. Type START to begin. Type HELP at any time for game instructions.")
	living_room = Location("Your Living Room", "You are in your living room. It is classy, but that makes sense. You're one of the first trillionaires to jump on the space travel market. You sure made a killing but that also makes sense. Tech was always your thing.")
	kitchen = Location("The Kitchen", "This is your kitchen. It is very large and very automated. If you wanted coffee you could ask your J.A.R.B.I.S. (or Just A Random Boy's Interpretive System). That is if you have him on you.")
	bedroom = Location("Your Bedroom", "This is your bedroom. Like all spaces in your skyrise building, it is very large. You see your king-size bed and other bedroomy things you would find in a bedroom.")
	workshop = Location("Your Workshop", "This is your workshop. Its where all the technical magic happens - and technically, it is magic what you do. Your workbench sits in the middle of the room while different instruments for producing your gagets rest against all 4 walls.")

	#items
	tablet = Item("schematic tablet", "A schematic tablet", "The schematic was developed by your parents Kel & Aurora LosForeve. You know it like the back of your hand.", 
		start_at=bedroom, gettable=False, get_fail="You already know the topic like the back of your hand so there's no need in taking it with you, but maybe you want to MOVE it off the floor?")
	keycard = Item("keycard", "A keycard to your workshop", "NFC protocols have been around for the last 200 years or so and really easy imitate using a replicator, but hey, its only for your workshop. No biggie.",
		use_fail="You definitely can use this but with what?"
		)
	keypad = Item("keypad", "A keypad to your workshop", "Its the locking mechanism to your workshop. Normally, your J.A.R.B.I.S controls it but since you can't find it, this will do.",
		start_at=living_room, gettable=False, get_fail="You consider ripping the keypad off your wall for a second, but a sober second thought tells you not to...",
		use_fail="You could use the keypad with your keycard, if you had it. But where is your keycard?")
	dead_jarbis = Item("jarbis", "Your J.A.R.B.I.S on the floor", "J.A.R.B.I.S., or Just A Random Boy's Interpretive System, is your personal natural language interpreter and assistant. It's like Siri or Alexa of the early 21st century, but cooler. It seems unresponsive though.",
		start_at=kitchen)
	jarbis = Item("jarbis", "Your J.A.R.B.I.S.", "Your J.A.R.B.I.S seems to be funcioning properly now.")
	workbench = Item("workbench", "your workbench", "Its where you do most of your tinkering. Really its just a desk with drawers. There are a few drawers you could OPEN if you wanted to sneak a peak inside your workbench. Could be fun.",
		start_at=workshop)
	screwdriver = Item("screwdriver", "A screwdriver.", "Now that you think about it, as much as technology has advanced, some thing just stay the same.")
	
	#item interactions (function sets up two-way relationship)
	keycard.add_interaction(keypad, s.toggle_room_condition, ("keypad_unlocked", "You press the keycard to the keypad and you hear the 'ch-chunk' of the workshop door unlocking", "You press the keycard to the keypad and hear the workshop door lock tight."),
		preconditions={"inventory_contains": keycard, "location_has_item": keypad})

	# connections
	bedroom.add_connection("east", living_room)
	living_room.add_connection("south", kitchen)
	living_room.add_connection("down", workshop)

	#room_conditions
	living_room.set_condition("keypad_unlocked", False)

	# blocks
	living_room.add_block("down", "Your workshop is locked and it seems the only in is through a key card. Now, if you could only remember where you put it...", preconditions={"room_condition_is_true": "keypad_unlocked"})
	
	# dialogue

	#special
	intro.add_action("start", s.move_to_room, (living_room, "To begin game, type START"))
	tablet.add_action("move tablet", s.perform_multiple_actions, 
		([(s.destroy_item, (tablet, "You decide to put the the tablet back on your shelf, and look! Its your keycard underneath!", "You already moved your tablet back to its rightful place.")),
		  (s.create_item, (keycard, "You can now take your keycard.", "You already grabbed your keycard."))
			]))
	# living_room.add_action("use keycard with keypad", s.toggle_room_condition, ("keypad_unlocked", "You press the keycard to the keypad and you hear the 'ch-chunk' of your workshop door unlocking.", "You press the keycard to the keypad and you hear the 'ch-chunk' of your workshop door locking."),
	# 	preconditions={"inventory_contains":keycard})
	#living_room.add_action("use keypad with keycard", s.toggle_room_condition, ("keypad_unlocked", "You press the keycard to the keypad and you hear the 'ch-chunk' of your workshop door unlocking.", "You press the keycard to the keypad and you hear the 'ch-chunk' of your workshop door locking."),
	#	preconditions={"inventory_contains":keycard})

	return Game(intro)

def main(game):
	lexicon = Lexicon("lexicon/test.json")
	parser = Parser(game, lexicon=lexicon)
	game.describe()

	command = ""
	while not (command.lower() == "exit" or command.lower == 'q'):
		command = input("> ")
		end_game = parser.parse_command(command)
		if end_game:
			return
	#game_loop()
	print("THE GAME HAS ENDED.")

if __name__ == '__main__':
	g = builder()
	main(g)