#!/usr/bin/env python3
#Run this file first and then the receiver as this defines the pipe
import os

pipe_name = "/tmp/my_program.fifo"
if not os.path.exists(pipe_name):
	os.mkfifo(pipe_name)
print('''
	Sending message acorss terminals
	(Run the receiver.py from the same folder on a new terminal) 
	''')
fifo = open(pipe_name, "w")# Note that here we are writing in the text for and no the binary form
fifo.write('How are you doing?\n')
fifo.close()

print('Message Sent! Check the receiver for output')

