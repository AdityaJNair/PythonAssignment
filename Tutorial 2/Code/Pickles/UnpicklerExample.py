#!/usr/bin/env python3

import pickle

print('Unpickling data...')
unpickleFile = open('pickle.pkl', 'rb')
retreivedList= pickle.load(unpickleFile) # this is where the object is deserialised
NameAgeThing= pickle.load(unpickleFile)
print('After unpickling, the list looks like:', retreivedList)
print('After unpickling, the NameAge thing looks like:', NameAgeThing)
