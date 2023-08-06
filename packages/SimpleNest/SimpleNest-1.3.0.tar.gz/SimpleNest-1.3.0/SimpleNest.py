def print_lol(the_list, indent = False,level=0,fh = sys.stdout) :
	'''This function takes a list(can have embedded list within) and print out each item. If there is an embedded one, level controls how many tabs used to print it.'''
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item,indent,level+1,fh)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end='',file = fh)
			print(each_item,file = fh)
