from lexicon.annotator import Annotator
from string import punctuation
import json

class Lexicon():
	"""This object can build the necessary synonyms and alternatives for in-game
	commands that your parser will be able to recognize."""
	def __init__(self, filename=None):
		direction =  {"north": "n", "east": "e", "south": "s", "west": "w",
			"northeast": "ne", "northwest": "nw", "southeast": "se",
			"southwest": "sw", "up": "up", "down": "down", "in": "in", "out": "out"}
		objects = {"keypad", "keycard", "jarvis", "screwdriver", "schematic tablet"}
		verbs = self.build_verbs_from_file(filename)
		prep_conj = {'and', 'with', "on"}
		stops = {'does', 'll', "didn't", 'am', 'was', 'own', 'same',
			'should', 'have', "you'd", 'd', 'y', "isn't", 'shan', 'over', 'after', 
			'ain', 'further', 'any', 'some', 'those', 'both', 'm', 'myself', 'more',
			'not', "haven't", "mustn't", 'how', 'had', 'having', 'herself',
			'when', 'yourselves', 'itself', "weren't", 'ours', 'do', 'shouldn', 'don',
			"you've", 'about', 'we', 'has', "shan't", 'weren', 'each', "needn't",
			'only', 'she', "hasn't", 'because', 'against', 'off', "wouldn't",
			'why', 'them', 'an', "shouldn't", "couldn't", 'into', 'too', 'he', 'ma',
			'isn', 'whom', "should've", 'are', 'which', 'at', 'it', 'who', 'doing',
			'below', 'doesn', 'if', 'most', 'his', 'through', 'hadn', 'won', 'again',
			'hers', 'her', 'during', 'or', 'your', 'this', 'nor', 'they', 'what', 'my',
			'themselves', 'under', 'in', 'but', "don't", 'their', "she's", 'wouldn',
			'from', 'were', 'by', 'me', 'himself', 'theirs', 'there', 'a', "you're",
			'ourselves', 'until', 'now', "wasn't", 'as', 'very', 'so', 'to', 'such',
			'once', 'i', "you'll", 'all', 'just', "it's", 'is', 'been', 'of',
			'these', 'where', "aren't", 'other', 'be', 'couldn', 'didn', 'while',
			'you', 'can', 'the', 'then', 'o', "doesn't", "won't", 'mustn',
			'mightn', 'our', 'haven', 'him', 'yourself', 'wasn', 's', 're',
			'did', 've', 'above', "hadn't", "mightn't", 'few', 'its', 'aren', 'for',
			'here', 'needn', 'before', 'yours', "that'll", 'than', 'between', 'will',
			'hasn', 't', 'that', 'being', 'no'}
		self.vocab = {"verb": verbs, "prep_conj": prep_conj, "stop":stops,
			"object": objects, "direction": direction }
		self.allowed = {("verb", "object"), 
			       ("verb", "direction"),
			       ("verb", "error"),
			       ("verb", "object", "prep_conj", "object"),
			       ("verb", "object", "prep_conj", "error"),
			       ("verb", "error", "prep_conj", "object"),
			       ("direction", ),
			       ("verb", )}

	def tokenize(self, command):
		word_list = command.lower().split()
		scanned = []
		for word in word_list:
			word = self.clean(word)
			for word_type in self.vocab:
				found = False
				# look for verb substitutions
				if word_type == "verb" or word_type == "direction":
					word = self.scan_substitute(word, word_type)

				if word in self.vocab[word_type]:
					scanned.append((word, word_type))
					found = True
					break

			if not found:
				scanned.append((word, "error"))
		return self.remove_stops(scanned)

	def scan_substitute(self, word_string, word_type):
		for vk in self.vocab[word_type].keys():
			if word_string in self.vocab[word_type][vk] or word_string == vk:
				return vk
		return word_string

	def clean(self, word_string):
		table = str.maketrans(dict.fromkeys(punctuation))
		return word_string.translate(table)

	def remove_stops(self, wordlist):
		"""Removes any words that is in the lexicon's
		stop words set."""
		cleaned_list = []
		for word in wordlist:
			if not word[1] == "stop":
				cleaned_list.append(word)
		return cleaned_list
			
	def add_object_name(self, name):
		self.vocab['object'].add(name)

	def build_verbs_from_file(self, filename=None):
		# Returns a dict full of synonyms from a json file that has been
		# created by the annotator already
		if not filename:
			return None

		verbs = {}
		# get data
		with open(filename) as fp:
			data = json.load(fp)

		# get terms from hypernyms, put into lexicon (only once)
		for k,v in data['hypernyms'].items():
			terms = []
			for hyper in v:
				i = hyper.index(".")
				word = hyper[0:i].replace("_", " ")
				if not (word in terms):
					terms.append(word)
			verbs[k] = terms

		# get terms from hyponyms, put into lexicon (only once)
		for k,v in data['hyponyms'].items():
			terms=[]
			for hypo in v:
				i = hypo.index(".")
				word = hypo[0:i].replace("_", " ")
				if not (word in terms):
					terms.append(word)
			verbs[k].extend(terms)

		return verbs

	def annotate_system_commands(self, commands):
		"""Run this to create hypo/hypernyms for in-game commands"""
		annotator = Annotator()
		annotator.annotate(commands)