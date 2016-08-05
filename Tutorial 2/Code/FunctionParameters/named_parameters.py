#!/usr/bin/env python3
'''

'''

first_simple_list = []
second_simple_list = []

def setup():
	for x in range(0, 5):
		first_simple_list.append(x)
		second_simple_list.append(x*x)

def get_last_element(simple_list, front=False):
	if len(simple_list) == 0:
		return

	index = 1 if front else -1
	return simple_list[index]

#Program starts HERE
if __name__ == '__main__':
	setup()
	while True:
		operation = input("Which list? First(1), second(2), quit(q): ")
		
		if operation == "q":
			break		
		
		operation = int(operation)

		retrieve = input("(h)ead or (t)ail?: ")
		
		if operation == 1:
			if retrieve == "t":
				print(get_last_element(first_simple_list))
			elif retrieve == "h":
				print(get_last_element(first_simple_list, front=True))	
			else:
				print("Invalid command")	
		elif operation == 2:
			if retrieve == "t":
				print(get_last_element(second_simple_list))
			elif retrieve == "h":
				print(get_last_element(second_simple_list, front=True))
			else:
				print("Invalid command")
		else:
			print("Invalid command")
	
	
	
