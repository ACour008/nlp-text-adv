# Maybe turn to its own class?

def check_preconditions(preconditions, game, print_failure_reasons=True):
	"""Checks whether the player has met all the specified preconditions."""
	all_conditions_met = True
	for check in preconditions:

		if check == "inventory_contains":
			item = preconditions[check]
			if not game.is_in_inventory(item):
				all_conditions_met = False
				if print_failure_reasons:
					print("You don't have the %s" % item.name)

		if check == "in_location":
			location = preconditions[check]
			if not game.curloc == location:
				all_conditions_met = False
				if print_failure_reasons:
					print("You can't do that here.")

		if check == "location_has_item":
			item = preconditions[check]
			if not item.name in game.curloc.items:
				all_conditions_met = False
				if print_failure_reasons:
					print("The %s isn't here." % item.name)

		if check == "room_condition_is_true":
			condition_name = preconditions[check]
			if condition_name in game.curloc.conditions:
				if not game.curloc.conditions[condition_name]:
					all_conditions_met = False
					if print_failure_reasons:
						print("This condition isn't set to true.")

		if check == "room_condition_is_false":
			condition_name = preconditions[check]
			if condition_name in game.curloc.conditions:
				if game.curloc.conditions[condition_name]:
					all_conditions_met = False
					if print_failure_reasons:
						print("This condition isn't set to false.")
	return all_conditions_met
