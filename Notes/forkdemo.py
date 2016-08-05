import os

i = 0
while i < 2:
    os.fork()
    os.system('ps -o pid,ppid,comm,stat')
    i += 1
