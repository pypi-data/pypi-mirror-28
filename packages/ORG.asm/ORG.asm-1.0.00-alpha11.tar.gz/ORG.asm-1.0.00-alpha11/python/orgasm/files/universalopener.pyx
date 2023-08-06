#cython: language_level=3

'''
Created on 25 mars 2016

@author: coissac
'''

from urllib.request import urlopen


    
def uopen(str name, mode='r', int buffersize=100000000):
    cdef CompressedFile c
    cdef LineBuffer lb
    
    try:
        f = urlopen(name)
    except:
        f = open(name,mode) 
        
    c = CompressedFile(f)
    
    if isinstance(c, LineBuffer):
        lb=c
    else:
        lb=LineBuffer(c,buffersize)
        
    i = iter(lb)
    
    return i
