import os
import sys
import pickle
import time
import threading
import atexit
from queue import Queue

#ANAI714
#6393001

#GLOBAL ANY VAR for any message
ANY = 'any'

#MessageProc Class
class MessageProc:
    #Queues and lists used in Receive implementation
    communication_queue = Queue()
    communication_list = []
    #Threading condition for notifying and syncing threads
    arrived_condition = threading.Condition()
    #fields used for timeout instantiation
    timeout_start = False
    timeout_data = None
    timeout_action = lambda: None
    timeout_reset_time = None

    '''
    The give message takes in a pid, label and multiple values
    It opens the pipe associated to the pid given and then opens the pipe and dumps the data by picking it
    '''
    def give(self, pid, label, *values):
        pipe_name = '/tmp/anai714%d.fifo' %(pid)
        if(os.path.exists(pipe_name)):
            with open(pipe_name, 'wb', buffering=0) as fifo:
                pickle.dump([label, values], fifo )

    '''
    The receive method first resets the timeout fields to its original after each iteration of the function.
    It then goes through all of the messages to store information on the first Timeout message
    '''
    def receive(self, *messages):
        #reset the timeout information
        self.reset()
        #iterate through messages to find timeout information
        for message in messages:
            if type(message) is TimeOut:
                self.timeout_data = message.data
                self.timeout_action = message.action
                self.timeout_start = True
                break
        #iterate forever
        while True:
            #check if the queue that gets the messages in from extract form pipe method is not empty
            #if it is not empty append it to the list inside this method
            while(self.communication_queue.qsize() != 0):
                self.communication_list.append(self.communication_queue.get())
            #iterate through the list (only done if sometihng inside the list) and go through the messages to find valid message
            for retreivedList in self.communication_list:
                for message in messages:
                    #Check is the message a message object
                    #Check if the data from the message matches the list message
                    #Check if the message is ANY
                    #Check if there is a guard
                    #If it is true then the message is valid
                    if (type(message) is Message and (((message.data == retreivedList[0]) or (message.data == ANY)) and message.guard())):
                        #remove from the list as seen and do the action of the message
                        self.communication_list.remove(retreivedList)
                        return message.action(*retreivedList[1])
            #This part will run if the queue is empty so we are waiting for another input as all others have been processed
            if self.communication_queue.qsize()==0:
                with self.arrived_condition:
                    #If we have a condition flag that there is a timeout so we need to check and time for the timeout
                    if self.timeout_start:
                        #start time at point when we find nothing
                        start_time = time.time()
                        #Wait for a message to arrive within the timout time given by the TimeOut object
                        check_if_notified = self.arrived_condition.wait(self.timeout_data)
                        end_time = time.time()
                        #Calculate the time that has passed based on how fast if a notification arrived or whole timeout time
                        self.timeout_data = self.timeout_data - (end_time - start_time)
                        #If we have no notification that there is a message arrived within the timeout, or the time value for the
                        #next iteration is 0 or less then run the action provided by the timeout object
                        if (not check_if_notified) or (self.timeout_data <= 0):
                            return self.timeout_action()
                    else:
                        #done if no timeout, so wait forever until message arrives
                        self.arrived_condition.wait()

    #reset helper method to reinstantiate the timeout fields
    def reset(self):
        self.timeout_start = False
        self.timeout_data = self.timeout_reset_time
        self.timeout_action = lambda: None

    #start the forking of the process and run the main of the child process, return the pid of the child to parent
    def start(self, *args):
        pid = os.fork()
        if(pid == 0):
            self.main(*args)
            sys.exit()
        else:
            time.sleep(0.1)
        return pid

    #main method to setup the pipes and run the thread
    def main(self, *args):
        #Creates a pipe with the pid of the process if no pipe is made
        pipe_name = '/tmp/anai714%d.fifo' %(os.getpid())
        if not os.path.exists(pipe_name):
            os.mkfifo(pipe_name)
        #Start the thread that goes to extract_from_pipe
        transfer_thread = threading.Thread(target=self.extract_from_pipe, daemon=True)
        transfer_thread.start()
        #at exit (sys.exit()) go to the close method
        atexit.register(self.close)

    #method given from Robert to process the messages from the file and put it in a queue
    def extract_from_pipe(self):
        '''
        Take all data in the pipe and transfer to the communications queue.
        The reason for this being in a separate thread is so that the load does not
        block the process and we can notify blocked receives.
        '''
        pipe_name = '/tmp/anai714%d.fifo' %(os.getpid())
        #print('{}  {} in extract'.format(os.getpid(), pipe_name))
        if(os.path.exists(pipe_name)):
            with open(pipe_name, 'rb', buffering=0) as pipe_rd:
                while True:
                    try:
                        message = pickle.load(pipe_rd)
                        with self.arrived_condition:
                            self.communication_queue.put(message)
                            self.arrived_condition.notify() #wake up anything waiting
                    except EOFError: #no writer open yet
                            time.sleep(0.01) # dont want to overload the cpu

    #At close remove the process pipes
    def close(self):
        path = '/tmp/anai714%d.fifo' % (os.getpid())
        if (os.path.exists(path)):
            os.remove(path)


'''
    Message field class that stores the fields for the messages used in receive() and give()
'''

#Message class
class Message:

    def __init__(self, data, action=lambda:None, guard=lambda:True):
        self.data = data
        self.action = action
        self.guard = guard

#TimeOut class
class TimeOut:

    def __init__(self, data, action=lambda:None):
        self.data = data
        self.action = action

