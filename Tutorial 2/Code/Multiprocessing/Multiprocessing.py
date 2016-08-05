#!/usr/bin/env python3

import multiprocessing,time,sys

def daemonJob(): #This will be preempted
    print ('I am Starting DaemonJob. My name is:', multiprocessing.current_process().name)
    time.sleep(3) #Simulating work 
    print ('I am Finishing DaemonJob. My name is: ', multiprocessing.current_process().name)

def nonDaemonJob(): #This will not be preempted
    print ('I am Starting nonDaemonJob. My name is:', multiprocessing.current_process().name)
    pass                 #Simulating work
    print ('I am Finishing nonDaemonJob. My name is :', multiprocessing.current_process().name)

if __name__ == '__main__': #Check to ensure that this code is run only by the main process and not by spawned processes.
    daemon_process = multiprocessing.Process(name='daemon', target=daemonJob) #Creating, naming and assigning a job to this thread
    daemon_process.daemon = True

    non_daemon_process = multiprocessing.Process(name='non-daemon', target=nonDaemonJob)
    #non_daemon_process.daemon = False        # By default the daemon property is set to false

    print('Triggering processes')
    
    daemon_process.start()         #triggering processes
    non_daemon_process.start()
    
    print('Processes have been triggered')
    #daemon_process.terminate() # you can terminate any process irrespective of their current exeution states
    daemon_process.join(1)
    
    print ('daemon_process.is_alive()', daemon_process.is_alive()) # For illustration purposest to demonstrate that the daemon process is alive when the program preempts it.
    
    non_daemon_process.join()


   

