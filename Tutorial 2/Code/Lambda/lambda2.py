#!/usr/bin/env python3

OPERATION_COUNT = 4
simple_collection_of_lambdas = [None] * OPERATION_COUNT

#set up the lambdas for calculator
def setup_lambdas():
	#add
	simple_collection_of_lambdas[0] = lambda x, y: x + y
	#subtract
	simple_collection_of_lambdas[1] = lambda x, y: x - y
	#multiply
	simple_collection_of_lambdas[2] = lambda x, y: x * y
	#divide
	simple_collection_of_lambdas[3] = divide

def divide(x, y):
	return (x / y)

if __name__ == '__main__':
	setup_lambdas()
	number_one = int(input("Enter the first number: "))
	number_two = int(input("Enter the second number: "))

	for x in range(0, OPERATION_COUNT):
		print(simple_collection_of_lambdas[x](number_one, number_two))


