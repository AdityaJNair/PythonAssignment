#!/usr/bin/env python3

import pickle

randomNumbers = [2,7,8,9,5,3,4,6]
NameAge = {'John':20,'Bob':22,'Alice':21}

print('Original list before pickling looks like:',randomNumbers)
pickleFile = open('pickle.pkl', 'wb')
pickle.dump(randomNumbers,pickleFile) #This is where the object is serialized
pickle.dump(NameAge,pickleFile) #Note that the objects can be dumped at one go as well using tuples
pickleFile.close()
print('Pickling is complete')

