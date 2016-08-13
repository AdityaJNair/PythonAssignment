import os
import sys
import pickle
import time

class MessageProc:
    ANY = True

    '''
        Sending a message
        pid = process id
        label = message name e.g. "data"
        *values = any additional values
        Gets the process id and the label which is the message and gives it
        to the other processor through a pipe
    '''
    def give(self, pid, label, *values):
        pipe_name = '/tmp/%d.fifo' %(os.getpid())
        fifo = open(pipe_name, 'wb')
        pickle.dump((pid, label, *values ), pipe_name )
        fifo.close()

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
        pipe_name = '/tmp/%d.fifo' %(os.getpid())
        fifo = open(pipe_name, 'rb')
        for message in messages:
            line = pickle.load(pipe_name)
            if os.getpid() == line[0]:
                if message.get_data_message == line[1] or message.get_data_message == ANY:
                    return message.getAction()()
        fifo.close()
    '''
        Starts the new process and returns the identifier
    '''
    def start(self, *args):
        pid = os.fork()
        if(pid == 0):
            self.main()
        else:
            return pid

    '''
        Sets up the communication
        setup method
    '''
    def main(self):
        #creates a pipe but if exists doesnt make another
        #for parent and child at same time
        #removes any previous pipes
        print(os.getpid())
        pipe_name = '/tmp/%d.fifo' %(os.getpid())
        if os.path.exists(pipe_name):
            os.remove(pipe_name)
            os.mkfifo(pipe_name)
        #initialise any fields inside MessageProc


'''
    Message field class that stores the fields for the messages used in receive() and give()
'''
class Message:
    data_message = ""
    action = None

    def __init__(self, data, action=None):
        self.data_message = data
        self.action = action

    def get_data_message(self):
        return self.data_message

    def get_action(self):
        return self.action