import os
import sys
import pickle
import time
import threading
import atexit
import re
from queue import Queue

#ANAI714
#6393001

#GLOBAL ANY VAR
ANY = 'any'
class MessageProc:

    communication_queue = Queue()
    arrived_condition = threading.Condition()
    communication_list = []
    time_out_val = 9999
    start_time = 0
    end_time = 0


    '''
        Sending a message
        pid = process id
        label = message name e.g. "data"
        *values = any additional values
        Gets the process id and the label which is the message and gives it
        to the other processor through a pipe
    '''
    def give(self, pid, label, *values):
        pipe_name = '/tmp/%d.fifo' %(pid)
        if(os.path.exists(pipe_name)):
            with open(pipe_name, 'wb') as fifo:
                tmp_list = []
                tmp_list.append(label)
                tmp_list.append(list(values))
                pickle.dump(tmp_list, fifo )
                #print('this is in get tmp')
                #print(tmp_list)
    '''
        In receive method we iterate through the *messages parameter
        and check the Message Objects made.
        Check the list of messages to see if there is one that matches a condition
        being waited for
        if it finds a match it removes the message and carries out any actions associated with the message
        Each receive only receives one message
        Returns the lamda thing
    '''
    def receive(self, *messages):
        while True:
            while(self.communication_queue.qsize() != 0):
                self.communication_list.append(self.communication_queue.get())
            if(len(self.communication_list) != 0):
                for retreivedList in self.communication_list:
                    for message in messages:
                        #check if first field is data a digit. If not do messages
                        if (message.guard()):
                            if (message.data == retreivedList[0]) or (message.data == ANY):
                                self.communication_list.remove(retreivedList)
                                return message.action(*retreivedList[1])
            else:
                with self.arrived_condition:
                    self.arrived_condition.wait(self.time_out_val)
            '''
        while True:
            if(self.communication_queue.qsize() != 0):
                if(self.communication_queue.qsize() != 0):
                    item = self.communication_queue.get()
                    self.communication_queue.task_done()
                    self.communication_list.append(item)
                elif(len(self.communication_list) != 0):
                    for retreivedList in self.communication_list:
                        for message in messages:
                            #check if first field is data a digit. If not do messages
                            if (message.guard()):
                                if (message.data == retreivedList[0]) or (message.data == ANY):
                                    self.communication_list.remove(retreivedList)
                                    return message.action(*retreivedList[1])
            else:
                with self.arrived_condition:
                    self.arrived_condition.wait()
            '''
    '''
        Starts the new process and returns the identifier
    '''
    def start(self, *args):
        pid = os.fork()
        if(pid == 0):
            self.main(*args)
        else:
            time.sleep(0.1)
        return pid
    '''
        Sets up the communication
        setup method
    '''
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



    '''
    from roberts lec
    '''
    def extract_from_pipe(self):
        '''
        Take all data in the pipe and transfer to the communications queue.
        The reason for this being in a separate thread is so that the load does not
        block the process and we can notify blocked receives.
        '''
        pipe_name = '/tmp/%d.fifo' %(os.getpid())
        #print('{}  {} in extract'.format(os.getpid(), pipe_name))
        if(os.path.exists(pipe_name)):
            with open(pipe_name, 'rb') as pipe_rd:
                while True:
                    try:
                        message = pickle.load(pipe_rd)
                        with self.arrived_condition:
                            #self.communication_list.append(message)
                            self.communication_queue.put(message)
                            self.arrived_condition.notify() #wake up anything waiting
                    except EOFError: #no writer open yet
                            time.sleep(0.1) # dont want to overload the cpu

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

@atexit.register
def close():
    path = '/tmp/%d.fifo' %(os.getpid())
    if (os.path.exists(path)):
            os.remove(path)
