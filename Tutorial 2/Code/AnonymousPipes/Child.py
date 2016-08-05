#!/usr/bin/env python3
'''
This file is just to be imported into parent file. 
You need not execute this!
'''
import os, time 

def child(pipeout):
	#Executes everytime its imported by the parent module
	someRandomTime = 1 
	while 1: 
		time.sleep(someRandomTime) 
		os.write(pipeout, bytes(someRandomTime)) 

	print('Unreacheable Code')
