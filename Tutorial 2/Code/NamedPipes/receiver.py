#!/usr/bin/env python3

import os
import sys

print('''
	Receiving messages accross terminals
	(If you see this for a really long time try running the sender.py in another terminal again)
	''')
pipe_name = "/tmp/my_program.fifo"
fifo = open(pipe_name, 'r')
for line in fifo:
    print('Received: ', line)
fifo.close()

