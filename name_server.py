import os
import sys
from process_message_system import *

class ServiceProvider(MessageProc):
    service_dictionary = {}

    #a user can register their information to the naming server by using their processid and their object type str(type(Object))
    #process id is the id of the service
    #object is the string name of that objecct
    def register(self, processid, object):
        self.service_dictionary.update({object, processid})
        pipe_name = '/tmp/nameserver.fifo'
        if (os.path.exists(pipe_name)):
            with open(pipe_name, 'wb', buffering=0) as fifo:
                pickle.dump([processid, object], fifo)

    #A process will send its pid and the object that it is looking for
    def grab_service(self, processid, object):
        #check name server for the list of services we have
        self.give(processid, object)

    def startserver(self):
        #initialise the server
        #give its own named pipe that other processors will know as hardcoded
        pipe_name = '/tmp/nameserver.fifo'
        if not os.path.exists(pipe_name):
            os.mkfifo(pipe_name)

    def give(self, pid, label, *values):


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

    def extract_from_pipe(self):
        '''
        Take all data in the pipe and transfer to the communications queue.
        The reason for this being in a separate thread is so that the load does not
        block the process and we can notify blocked receives.
        '''
        pipe_name = '/tmp/nameserver.fifo'
        #print('{}  {} in extract'.format(os.getpid(), pipe_name))
        if(os.path.exists(pipe_name)):
            with open(pipe_name, 'rb', buffering=0) as pipe_rd:
                while True:
                    try:
                        message = pickle.load(pipe_rd)
                        with self.arrived_condition:
                            #self.communication_list.append(message)
                            self.communication_queue.put(message)
                    except EOFError: #no writer open yet
                            time.sleep(0.01) # dont want to overload the cpu



class A():
    processid = os.getpid()
    service_name = "A"

class B():
    processid = os.getpid()
    service_name = "B"

class C():
    processid = os.getpid()
    service_name = "C"

class D():
    processid = os.getpid()
    service_name = "D"


if __name__=='__main__':

