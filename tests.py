from location import Location
from lexicon import lexicon as l
from game import Game
from item import Item
from parser import Parser
import special as s

location = Location("Room", "A Very Nice Room.")
other_location = Location("Another Room", "Another Very Nice Room.")
lex = l.Lexicon("lexicon/test.json")
game = Game(location)
parser = Parser(game, lexicon=lex)
keycard = Item("keycard", "A keycard to your workshop", "NFC protocols have been around for the last 200 years or so and really easy imitate using a replicator, but hey, its only for your workshop. No biggie.",
		use_fail="You definitely can use this but with what?", start_at=location
		)
keypad = Item("keypad", "A keypad to your workshop", "Description", start_at=location, gettable=False)

location.add_connection("north", other_location)

keycard.add_interaction(keypad, s.toggle_room_condition, ("keypad_unlocked", "You press the keycard to the keypad and you hear the 'ch-chunk' of the workshop door unlocking", "You press the keycard to the keypad and hear the workshop door lock tight."),
		preconditions={"inventory_contains": keycard, "location_has_item": keypad})

command = "take keycard and keypad"
parsed = parser.parse_command(command)
command = "take keycard"
parsed = parser.parse_command(command)
command = "drop keycard and keypad"
parsed = parser.parse_command(command)