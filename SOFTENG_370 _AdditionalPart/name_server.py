import os
import sys
import pickle
import time
import threading
import atexit
import re
from queue import Queue
import math

class ServiceProvider():
    service_dictionary = {}
    communication_queue = Queue()
    communication_list = []
    arrived_condition = threading.Condition()



    def startserver(self):
        #initialise the server
        #give its own named pipe that other processors will know as hardcoded
        pipe_name = '/tmp/nameserver.fifo'
        if not os.path.exists(pipe_name):
            os.mkfifo(pipe_name)
        transfer_thread = threading.Thread(target=self.extract_from_pipe, daemon=True)
        transfer_thread.start()
        for _ in range(4):
            self.receive(
                Message(
                    'register',
                    action=lambda object,id: self.set_in_reg(object,id)),
                Message(
                    'grab',
                    action=lambda return_to_user,object,processid_of_object: self.give_service_id_back(return_to_user,object, processid_of_object)))
        atexit.register(self.close)
        sys.exit()


    def set_in_reg(self, object, id):
        self.service_dictionary[object] = id
        print('Added '+str(object)+' with process id of '+str(id))
        print('\nService to Address index')
        for i in self.service_dictionary:
            print('Dictionary input ' + i, self.service_dictionary[i])
        print('\n')
        self.give(object, 'accepted', 'your registration has been accepted by ServiceProvider')

    def give_service_id_back(self, return_to_user,object,processid_of_object):
        self.give(return_to_user, 'found_service', processid_of_object)
        print('Sending ' +str(object) + ' with address ' + str(processid_of_object) + ' back to user ' + str(return_to_user))

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
                    if (message.data == retreivedList[0] == 'register'):
                        self.communication_list.remove(retreivedList)
                        return message.action(retreivedList[1][0], retreivedList[1][1])
                    if (message.data == retreivedList[0] == 'grab'):
                        self.communication_list.remove(retreivedList)
                        objectid = self.service_dictionary[retreivedList[1][1]]
                        return message.action(retreivedList[1][0],retreivedList[1][1],objectid)
            if self.communication_queue.qsize()==0:
                with self.arrived_condition:
                        self.arrived_condition.wait()


    def extract_from_pipe(self):
        '''
        Take all data in the pipe and transfer to the communications queue.
        The reason for this being in a separate thread is so that the load does not
        block the process and we can notify blocked receives.
        '''
        pipe_name = '/tmp/nameserver.fifo'
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
        path = '/tmp/nameserver.fifo'
        if (os.path.exists(path)):
            os.remove(path)

class Message:

    def __init__(self, data, action=lambda:None, guard=lambda:True):
        self.data = data
        self.action = action
        self.guard = guard

if __name__=='__main__':
    me = ServiceProvider()
    me.startserver()

