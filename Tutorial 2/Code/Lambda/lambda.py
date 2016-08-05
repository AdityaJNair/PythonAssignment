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
	simple_collection_of_lambdas[3] = lambda x, y: x / y

if __name__ == '__main__':
	setup_lambdas()
	operation = int(input("What would you like to do? Add(1), subtract(2), multiply(3), divide(4): "))
	number_one = int(input("Enter the first number: "))
	number_two = int(input("Enter the second number: "))

	try:
		if(operation > 0 and operation < 5):
			print("Result: ", simple_collection_of_lambdas[operation-1](number_one, number_two))
	except Exception:
		print("Error occured...")


