#!/usr/bin/env python3
import os
import sys
import time

'''
	Basic python fork
'''

cake = 0;

def child():
	#prints the current process's PID
	print("A new child with PID: ", os.getpid())
	print("Child sees ", cake, " cakes")
	#kills itself
	sys.exit(0)

#forks the parent thread
def fork():
	#pid will be 0 for the child process and will be the child's pid for the parent process
	pid = os.fork()

	#Check if it is a child process
	if pid == 0:
		child()
	else:
		print ("Parent thread with PID: ", os.getpid())
		print ("The child will have PID: ", pid)
		print ("Parent sees ", cake, " cakes")


#Program starts HERE
if __name__ == '__main__':
	while True:
		time.sleep(1)
		command = input("What would you like to do? \n f: fork \n q: quit\n")
		#Execute fork
		if command == "f":
			fork()
			cake += 1
		#Exit program
		elif command == "q":
			break
		else:
			print("Invalid command")
