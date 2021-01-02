import textwrap

def wrap(text, length=80, end="\n"):
	for line in textwrap.wrap(text, length):
		print(line, end=end)