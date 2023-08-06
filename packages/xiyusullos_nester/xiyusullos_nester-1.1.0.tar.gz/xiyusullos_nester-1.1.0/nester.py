"""This is the "nester.py" module and it provides one function called print_lol() which prints lists that may or may not include nested lists."""
def print_lol(the_list, level):
	"""This function takes one positional argument called "the list", which is an any Python list (of - possibly - nested list). Each data item in the provided list is (recursively) printed to the screen on it's own line."""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, level + 1)
		else:
			# for tab_stop in range(level):
			# 	print('\t', end='')
			print('\t'*level, end='')
			print(each_item)