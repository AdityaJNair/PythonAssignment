#!/usr/bin/env python3
import os
import sys
import time

def fork_and_print():
	i=0
	while i < 4:
		pid = os.fork()
		if pid == 0:
			print(i)	
		i += 1

if __name__ == '__main__':
	fork_and_print()
	time.sleep(1)
	





