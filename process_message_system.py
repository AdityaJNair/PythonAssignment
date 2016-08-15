import os
import sys
import pickle
import time
import re

class MessageProc:
    ANY = True
    pidParent = 0
    pidChild = 0

    '''
        Sending a message
        pid = process id
        label = message name e.g. "data"
        *values = any additional values
        Gets the process id and the label which is the message and gives it
        to the other processor through a pipe
    '''
    def give(self, pid, label, *values):
        pipe_out = '/tmp/%d.fifo' %(pid)
        fifo_in = open(pipe_out, "w")
        #fifo_in.write('\"%s\" \"%s\" \n' %(label, list(values)))
        fifo_in.write('\'hello\' \'one\'\n')
        fifo_in.close()
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
        pipe_in = '/tmp/%d.fifo' %(os.getpid())
        fifo_out = open(pipe_in, 'r')
        for line in fifo_out:
            print(line)
            line = re.findall('"([^"]*)"', line)
            print(line)
            for m in messages:
                print('%s == %s' % (line[0], m.get_data_message()))
                if m.get_data_message() == line[0]:
                    return m.get_action()(line[1])
        fifo_out.close()

    '''
        Starts the new process and returns the identifier
    '''
    def start(self, *args):
        pid = os.fork()
        if not (pid == 0):
            return pid
        else:
            self.main()

    '''
        Sets up the communication
        setup method
    '''
    def main(self):
        #creates a pipe but if exists doesnt make another
        #for parent and child at same time
        #removes any previous pipes
        pipe_name = '/tmp/%d.fifo' %(os.getpid())
        if not os.path.exists(pipe_name):
            os.mkfifo(pipe_name)
        else:
            os.remove(pipe_name)
            os.mkfifo(pipe_name)
        if self.pidParent == 0:
            self.pidParent = os.getpid()
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