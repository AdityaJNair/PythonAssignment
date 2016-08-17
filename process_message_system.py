import os
import sys
import pickle
import time
import threading
import atexit
import re
from queue import Queue
import math

#ANAI714
#6393001

#GLOBAL ANY VAR
ANY = 'any'
class MessageProc:

    communication_queue = Queue()
    arrived_condition = threading.Condition()
    communication_list = []
    timeout_start = False
    timeout_data = None
    timeout_action = lambda: None
    timeout_reset_time = None

    def give(self, pid, label, *values):
        pipe_name = '/tmp/%d.fifo' %(pid)
        if(os.path.exists(pipe_name)):
            with open(pipe_name, 'wb', buffering=0) as fifo:
                pickle.dump([label, values], fifo )
                #print('this is in get tmp')
                #print(tmp_list)

    def receive(self, *messages):
        self.reset()
        for message in messages:
            if type(message) is TimeOut:
                self.timeout_data = message.data
                self.timeout_action = message.action
                self.timeout_start = True
                break
        #print('end time ' + str(self.timeout_end_time) + ' start time ' + str(
        #self.timeout_start_time) + ' end-start ' + str(self.timeout_end_time - self.timeout_start_time))
        while True:
            while(self.communication_queue.qsize() != 0):
                self.communication_list.append(self.communication_queue.get())
            for retreivedList in self.communication_list:
                for message in messages:
                #check if first field is data a digit. If not do messages
                    if (type(message) is Message and (((message.data == retreivedList[0]) or (message.data == ANY)) and message.guard())):
                        self.communication_list.remove(retreivedList)
                        return message.action(*retreivedList[1])
            if self.communication_queue.qsize()==0:
                with self.arrived_condition:
                    if self.timeout_start:
                        start_time = time.time()
                        check_if_notified = self.arrived_condition.wait(self.timeout_data)
                        end_time = time.time()
                        self.timeout_data = self.timeout_data - (end_time - start_time)
                        if (not check_if_notified) or (self.timeout_data <= 0):
                            return self.timeout_action()
                    else:
                        self.arrived_condition.wait()

    def reset(self):
        self.timeout_start = False
        self.timeout_data = self.timeout_reset_time
        self.timeout_action = lambda: None

    def start(self, *args):
        pid = os.fork()
        if(pid == 0):
            self.main(*args)
            sys.exit()
        else:
            time.sleep(0.1)
        return pid

    def main(self, *args):
        #creates a pipe but if exists doesnt make another
        #for parent and child at same time
        #removes any previous pipes
        pipe_name = '/tmp/%d.fifo' %(os.getpid())
        if not os.path.exists(pipe_name):
            os.mkfifo(pipe_name)
        #initialise any fields inside MessageProc
        transfer_thread = threading.Thread(target=self.extract_from_pipe, daemon=True)
        transfer_thread.start()
        atexit.register(self.close)

    def extract_from_pipe(self):
        '''
        Take all data in the pipe and transfer to the communications queue.
        The reason for this being in a separate thread is so that the load does not
        block the process and we can notify blocked receives.
        '''
        pipe_name = '/tmp/%d.fifo' %(os.getpid())
        #print('{}  {} in extract'.format(os.getpid(), pipe_name))
        if(os.path.exists(pipe_name)):
            with open(pipe_name, 'rb', buffering=0) as pipe_rd:
                while True:
                    try:
                        message = pickle.load(pipe_rd)
                        with self.arrived_condition:
                            #self.communication_list.append(message)
                            self.communication_queue.put(message)
                            #end time if a message comes in
                            #need to create time here
                            self.arrived_condition.notify() #wake up anything waiting
                    except EOFError: #no writer open yet
                            time.sleep(0.01) # dont want to overload the cpu

    def close(self):
        path = '/tmp/%d.fifo' % (os.getpid())
        if (os.path.exists(path)):
            os.remove(path)


'''
    Message field class that stores the fields for the messages used in receive() and give()
'''
class Message:

    def __init__(self, data, action=lambda:None, guard=lambda:True):
        self.data = data
        self.action = action
        self.guard = guard

class TimeOut:

    def __init__(self, data, action=lambda:None):
        self.data = data
        self.action = action

