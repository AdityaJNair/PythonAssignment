#!/usr/bin/env python3

import multiprocessing

class Worker(multiprocessing.Process):

    def run(self):
        print ('Hi! I am a worker. My name is ', self.name)
        return

if __name__ == '__main__':
    listOfBusyWorkers = []   #List indicating the number of workers that are busy at the moment.
    totalWorkers=5
    
    for numberOfWorkers in range(totalWorkers):
        thisWorker = Worker()
        listOfBusyWorkers.append(thisWorker)     #Assign this worker to the list of jobs 
        thisWorker.start()

    print('Workers have been assigned jobs')
    
    for everyworker in listOfBusyWorkers:
        everyworker.join() #Note that if the join function does not have any parameters, it can then wait indefinitely for the processes to end.

    print('All workers finished their jobs')