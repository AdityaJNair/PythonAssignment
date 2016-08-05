#!/usr/bin/env python3

dividend = int(input("Dividend: "))
divisor = int(input("Divisor: "))

try:
	print(dividend / divisor)
except ZeroDivisionError:
	print("You cannot divide by zero!")
