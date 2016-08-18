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

class ServiceB():
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
    starts up the service by creating a pipe for it based on the name of the Class
    Starts the thread going to extract on pipe method
    GIVES a message to the 'nameserver' that runs a REGISTER with itself as the Object and its pipe address
    '''
    def start_service(self):
        self.service_name = '/tmp/'+str(type(self).__name__)+'.fifo'
        if not os.path.exists(self.service_name):
            os.mkfifo(self.service_name)
        transfer_thread = threading.Thread(target=self.extract_from_pipe, daemon=True)
        transfer_thread.start()
        time.sleep(1)
        atexit.register(self.close)
        #THE PROTOCOL QUERY that will be used
        #(NAMESRVER NAME, REGISTER QUERY, NAME OF CLASS, PATH OF PIPE OF CLASS)
        self.give('nameserver', 'register', str(type(self).__name__), self.service_name)
        #This will run forever since its a service, but there is a timeout that exits the process in 10 seconds if no messages come in
        #which will always happen since there are no messages going to the service (only one from the nameserver after the give)
        while True:
            self.receive(
                Message(
                    ANY,
                    action=lambda x: print(x)),
                TimeOut(10, action=lambda: sys.exit()))

    #Gives the informationt o be sent to the pipe through pickling
    def give(self, pipe_address, label, *values):
        #sets the address as the pipe_address for the pipe
        pipe_name = '/tmp/'+str(pipe_address)+'.fifo'
        if (os.path.exists(pipe_name)):
            with open(pipe_name, 'wb', buffering=0) as fifo:
                pickle.dump([label, values], fifo)

    '''
           The receive method first resets the timeout fields to its original after each iteration of the function.
           It then goes through all of the messages to store information on the first Timeout message
           '''

    def receive(self, *messages):
        # reset the timeout information
        self.reset()
        # iterate through messages to find timeout information
        for message in messages:
            if type(message) is TimeOut:
                self.timeout_data = message.data
                self.timeout_action = message.action
                self.timeout_start = True
                break
        # iterate forever
        while True:
            # check if the queue that gets the messages in from extract form pipe method is not empty
            # if it is not empty append it to the list inside this method
            while (self.communication_queue.qsize() != 0):
                self.communication_list.append(self.communication_queue.get())
            # iterate through the list (only done if sometihng inside the list) and go through the messages to find valid message
            for retreivedList in self.communication_list:
                for message in messages:
                    # Check is the message a message object
                    # Check if the data from the message matches the list message
                    # Check if the message is ANY
                    # Check if there is a guard
                    # If it is true then the message is valid
                    if (type(message) is Message and (
                                ((message.data == retreivedList[0]) or (message.data == ANY)) and message.guard())):
                        # remove from the list as seen and do the action of the message
                        self.communication_list.remove(retreivedList)
                        return message.action(*retreivedList[1])
            # This part will run if the queue is empty so we are waiting for another input as all others have been processed
            if self.communication_queue.qsize() == 0:
                with self.arrived_condition:
                    # If we have a condition flag that there is a timeout so we need to check and time for the timeout
                    if self.timeout_start:
                        # start time at point when we find nothing
                        start_time = time.time()
                        # Wait for a message to arrive within the timout time given by the TimeOut object
                        check_if_notified = self.arrived_condition.wait(self.timeout_data)
                        end_time = time.time()
                        # Calculate the time that has passed based on how fast if a notification arrived or whole timeout time
                        self.timeout_data = self.timeout_data - (end_time - start_time)
                        # If we have no notification that there is a message arrived within the timeout, or the time value for the
                        # next iteration is 0 or less then run the action provided by the timeout object
                        if (not check_if_notified) or (self.timeout_data <= 0):
                            return self.timeout_action()
                    else:
                        # done if no timeout, so wait forever until message arrives
                        self.arrived_condition.wait()

    # reset helper method to reinstantiate the timeout fields
    def reset(self):
        self.timeout_start = False
        self.timeout_data = self.timeout_reset_time
        self.timeout_action = lambda: None

    #method given from Robert to process the messages from the file and put it in a queue
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


#START UP SERVICE B
if __name__=='__main__':
    me = ServiceB()
    me.start_service()
