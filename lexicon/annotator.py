from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import json

class Annotator:

	def __init__(self):
		self.confirmed_hyponyms = {}
		self.confirmed_hypernyms = {}
		self.word_sense = None

	def get_synonyms(self, word_sense):
		synonyms = []
		for lemma in word_sense.lemmas():
			synonym = lemma.name().replace('_', ' ')
			synonyms.append(synonym)
		return synonyms

	def annotate(self, commands, save_when_done=True):
		# Run this when you want to annotate new in-game commands.
		a = Annotator()
		self.word_senses = a.annotate_synsets(commands)
		for word in self.word_senses:
			print("First, pick the proper definition for the word {0}".format(word))
			print("===============")
			word_sense = wn.synset(self.word_senses[word])
			print("\nNext, pick which hypernyms of %s we should allow the player to use." % word_sense.name())
			print("===============")
			self.confirmed_hypernyms[word] = a.confirm_hyponyms(word, word_sense, do_hypernyms_instead=True)
			print("\nFinally, pick which hyponyms of %s we should allow player to use." % word_sense.name())
			print("===============")
			self.confirmed_hyponyms[word] = a.confirm_hyponyms(word, word_sense)
		print("Congrats, you are done annotating.")
		print("Enter a filename with .json extension to save your annotated commands.")
		
		if save_when_done:
			filename = ""
			while filename == "":
				filename = input("> ")
				if not filename:
					print("Enter a filename with a .json extension to save your annotated commands.")
			self.save(filename)


	def save(self, filename):
		data = {}
		data['word_senses'] = self.word_senses
		data['hypernyms'] = self.confirmed_hypernyms
		data['hyponyms'] = self.confirmed_hyponyms

		with open(filename, "w") as fp:
			fp.write(json.dumps(data, sort_keys=True, indent=4))
			fp.write("\n")
		print("{0} successfully saved.".format(filename))

	def annotate_synsets(self, sentences):
		"""This function queries WordNet for each word in a list of sentences,
		and asks the user to input a number corresponding to the synset."""

		word_senses = {}
		# Cached selections maps from word string to the previous
		# selection for this word (an integer)
		cached_selections = {}

		for i, sent in enumerate(sentences):
			words = word_tokenize(sent.lower())

			for word in words:
				synsets = wn.synsets(word)
				if len(synsets) != 0:
					selection = self.select_synset(sent, word, synsets, cached_selections)
					if selection != None:
						cached_selections[word] = selection
						if selection < len(synsets):
							s = synsets[selection]
							word_senses[word] = s.name()
		return word_senses

	def select_synset(self, sent, word, synsets, cached_selections):
		"""Ask user to select which sense of the word is being used
		in each sentence."""
		print(sent)
		print(word.upper())

		prev_selection = -1
		if word in cached_selections:
			prev_selection = cached_selections[word]

		for choice, s in enumerate(synsets):
			if choice == prev_selection:
				print("*** ", end='')
			print("%d) %s - %s" % (choice, s.name(), s.definition()))

		choice += 1
		if choice == prev_selection:
			print("*** ", end='')
		print("%d) None of these." % choice)

		selection = -1
		while selection == -1:
			try:
				user_input = input("> ")
				if user_input.strip() == 'x':
					# User can press 'x' to exit.
					return None
				if user_input.strip() == '' and prev_selection > -1:
					#User can press return to confirm previous selection.
					return prev_selection
				selection = int(user_input)
			except:
				selection = -1
			if selection < 0 or selection > len(synsets):
				print("Please select a number between 0-%d, or type 'x' to exit." % len(synsets))
				if prev_selection > -1:
					print("You can also press return to confirm the previous selection (marked by ***).")
			else:
				return selection

	def confirm_hyponyms(self, word, synset, do_hypernyms_instead=False):
		"""Ask the user to confirm which of hte hyponyms are applicable
		for this sentence."""
		print(word.upper())

		confirmed = []
		if do_hypernyms_instead:
			unconfirmed = synset.hypernyms()
		else:
			unconfirmed = synset.hyponyms()

		while len(unconfirmed) > 0:
			s = unconfirmed.pop(0)
			print("Is %s an appropriate substitute for %s? (y/n)" % (s.name(), word))
			print("It means: ", s.definition())
			print("Synonyms are: ", self.get_synonyms(s))
			user_input = ''
			while user_input == '':
				user_input = input("> ")
				user_input = user_input.strip()
				if user_input == 'y' or user_input == 'yes':
					confirmed.append(s.name())
					if do_hypernyms_instead:
						unconfirmed.extend(s.hypernyms())
					else:
						unconfirmed.extend(s.hyponyms())

				elif user_input == 'n' or user_input == 'no':
					pass
				elif user_input == 'x':
					# The user can press 'x' to exit
					return confirmed
				else:
					print("Please type 'yes', 'no', or 'x' to stop confirming this word")
					user_input = ''
		return confirmed