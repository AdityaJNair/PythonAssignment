#!/usr/bin/env python3

fruit_basket = {
	'Apples' : 5,
	'Bananas' : 10,
	'Lemons' : 1,
	'Pineapples' : 2,
	'Melons' : 3
}

fruit_basket['Oranges'] = 3
fruit_basket.pop("Apples")

for fruit, count in fruit_basket.items():
	print ("There are", count, fruit)	