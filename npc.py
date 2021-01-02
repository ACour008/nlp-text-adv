from item import Item

class NPC(Item):
	""" This is technically an Item object that the player will be able to
	interact with."""

	def __init__(self,
				name,
				description,
				examine_text="",
				take_text="",
				start_at=None,
				gettable=False,
				get_fail="",
				end_game=False):
		super().__init__(name, description, examine_text,
			take_text, start_at, gettable, get_fail, end_game)



