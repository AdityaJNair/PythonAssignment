#!/usr/bin/env python3

'''
	Deomnstrating variable parameters
'''

CHEF_COOK = 1
CHEF_FRY = 2
CHEF_MICROWAVE = 3

def do_chef_things( action, ingredients, *extras):
	if action == CHEF_COOK:
		print("Cooking with ...")
	elif action == CHEF_FRY:
		print("Frying with ...")
	elif action == CHEF_MICROWAVE:
		print("Microwaving with ...")
	else:
		print("Not sure what I'm doing with ...")

	#iterate over all the ingredients
	for ingredient in ingredients:
		print(ingredient)

	print("with extra...")
	#iterate over all the extras
	for extra in extras:
		print(extra)

	print("Cooking done!")
		

#Program starts HERE
if __name__ == '__main__':
	print("Chef is ready")
	ingredients = []
	while True:
		command = input("Enter some ingredients or press c to continue: ")
		if command == "c":
			break
		else:
			ingredients.append(command)


	chef_action = int(input("Would you like it cooked(1), fried(2) or microwaved(3): "))
	extra_option = int(input("Would you like extra salt(1), pepper(2), both(3) or none(4): "))

	if extra_option == 1:
		do_chef_things(chef_action, ingredients, "salt")
	elif extra_option == 2:
		do_chef_things(chef_action, ingredients, "pepper")
	elif extra_option == 3:
		do_chef_things(chef_action, ingredients, "salt", "pepper")
	elif extra_option == 4:
		do_chef_things(chef_action, ingredients)
