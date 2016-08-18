import os
import sys
import pickle
import time
import threading
import atexit
from queue import Queue
ANY='any'

#ANAI714
#6393001

class ConsumerA():
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
    starts up the consumer by creating a pipe for it based on the name of the Class
    Starts the thread going to extract on pipe method
    GIVES a message to the 'nameserver' that runs a GRAB with the object it is looking for as the Object and consumer Name which will be used to open its pipe
    '''
    def start_consumer(self):
        self.consumer_name = '/tmp/'+str(type(self).__name__)+'.fifo'
        if not os.path.exists(self.consumer_name):
            os.mkfifo(self.consumer_name)
        #Start threading into the extract from pipe method
        transfer_thread = threading.Thread(target=self.extract_from_pipe, daemon=True)
        transfer_thread.start()
        time.sleep(1)
        #the protocol to send to the nameserver
        #(NAMESERVER, GRAB TO GET SERVICE ADDRESS, MY CONSUMER CLASS NAME, SERVICE I WANT TO GET THE ADDRESS OF)
        self.give('nameserver', 'grab', str(type(self).__name__), 'ServiceA')
        self.receive(
            Message(
                ANY,
                action=lambda x: print(x)))
        atexit.register(self.close)
        sys.exit()

    #Gives the informationt o be sent to the pipe through pickling
    def give(self, pipe_address, label, *values):
        pipe_name = '/tmp/'+str(pipe_address)+'.fifo'
        if (os.path.exists(pipe_name)):
            with open(pipe_name, 'wb', buffering=0) as fifo:
                pickle.dump([label, values], fifo)

    #simple receive that has no timeouts that checks if a message is valid
    #Will never take in a timeout message as it executes instantly
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

    #method given from Robert to process the messages from the file and put it in a queue
    def extract_from_pipe(self):
        '''
        Take all data in the pipe and transfer to the communications queue.
        The reason for this being in a separate thread is so that the load does not
        block the process and we can notify blocked receives.
        '''
        pipe_name = self.consumer_name
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

    # At close remove the process pipes
    def close(self):
        path = '/tmp/'+str(type(self).__name__)+'.fifo'
        if (os.path.exists(path)):
            os.remove(path)

#Message class
class Message:

    def __init__(self, data, action=lambda:None,guard=lambda:True):
        self.data = data
        self.action = action
        self.guard = guard

#TimeOut class
class TimeOut:

    def __init__(self, data, action=lambda:None):
        self.data = data
        self.action = action

#CREATE A CONSUMER A
if __name__=='__main__':
    me = ConsumerA()
    me.start_consumer()
