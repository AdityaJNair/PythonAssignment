import os
import sys
import pickle
import time
import threading
import atexit
import re
from queue import Queue
import math
ANY='any'

class ConsumerB():
    service_dictionary = {}
    communication_queue = Queue()
    communication_list = []
    arrived_condition = threading.Condition()




    def start_consumer(self):
        #initialise the server
        #give its own named pipe that other processors will know as hardcoded
        self.service_name = '/tmp/'+str(type(self).__name__)+'.fifo'
        if not os.path.exists(self.service_name):
            os.mkfifo(self.service_name)
        transfer_thread = threading.Thread(target=self.extract_from_pipe, daemon=True)
        transfer_thread.start()
        time.sleep(1)

        self.give('nameserver', 'grab', str(type(self).__name__), 'ServiceB')
        self.receive(
            Message(
                ANY,
                action=lambda x: print(x)))
        atexit.register(self.close)
        sys.exit()

    def give(self, pipe_address, label, *values):
        pipe_name = '/tmp/'+str(pipe_address)+'.fifo'
        if (os.path.exists(pipe_name)):
            with open(pipe_name, 'wb', buffering=0) as fifo:
                pickle.dump([label, values], fifo)

    def receive(self, *messages):
        while True:
            while(self.communication_queue.qsize() != 0):
                self.communication_list.append(self.communication_queue.get())
            for retreivedList in self.communication_list:
                for message in messages:
                    #if register
                    if (type(message) is Message and message.data == ANY):
                        self.communication_list.remove(retreivedList)
                        return message.action(*retreivedList[1])
            if self.communication_queue.qsize()==0:
                with self.arrived_condition:
                        self.arrived_condition.wait()


    def extract_from_pipe(self):
        '''
        Take all data in the pipe and transfer to the communications queue.
        The reason for this being in a separate thread is so that the load does not
        block the process and we can notify blocked receives.
        '''
        pipe_name = self.service_name
        if(os.path.exists(pipe_name)):
            with open(pipe_name, 'rb', buffering=0) as pipe_rd:
                while True:
                    try:
                        message = pickle.load(pipe_rd)
                        with self.arrived_condition:
                            #self.communication_list.append(message)
                            self.communication_queue.put(message)
                            self.arrived_condition.notify()  # wake up anything waiting
                    except EOFError: #no writer open yet
                            time.sleep(0.01) # dont want to overload the cpu

    def close(self):
        path = '/tmp/'+str(type(self).__name__)+'.fifo'
        if (os.path.exists(path)):
            os.remove(path)

class Message:

    def __init__(self, data, action=lambda:None, guard=lambda:True):
        self.data = data
        self.action = action
        self.guard = guard

if __name__=='__main__':
    me = ConsumerB()
    me.start_consumer()
