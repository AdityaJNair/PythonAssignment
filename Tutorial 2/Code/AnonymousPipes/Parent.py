#!/usr/bin/env python3
'''
Execute this file after giving the required permissions. 
'''

import os 
import Child	#This is yet another way to import a module and all it functions
def parent(): 
	pipein, pipeout = os.pipe() # Defining the anonymous pipe
	processID = os.fork()	#Forking out the child process
	if processID == 0: 		#Checking whether the current process is a parent or child
		Child.child(pipeout) 		#if child then call the code that needs to be run by child
	else:  
		while True: 		#else the parent performs the following tasks 
			line = os.read(pipein, 8) # reading from the pipe
			print ('Parent is continuously receiving the message: ', line)  #printing what it just read from the pipe

parent() 