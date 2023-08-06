#cython: language_level=3
from cpython.array cimport array

from orgasm.files.universalopener import uopen


def readFastq(filename):
    
    cdef str   line
    cdef bytes bline
    cdef bytes sid
    
    cdef int   seqid = 0
    cdef int   cut_slash
    cdef int   cut_space
    
    cdef array quality
    
    cdef bytes seq
    
    if isinstance(filename, str):
        filename = uopen(filename)
            
    for line in filename:
        bline = bytes(line,
                      encoding='ascii'
                     )
                
        while(bline[0]!=64):   # ord(b'@')
            bline = bytes(next(filename),
                          encoding='ascii'
                         )
            
        seqid+=1
        
        cut_space = bline.find(b' ')
        cut_slash = bline.find(b'/')
        if cut_space >= 0 :
            if cut_space < cut_slash or cut_slash < 0:
                sid = bline[1:cut_space]
            else:
                sid = bline[1:cut_slash]
        elif cut_slash >= 0:
            sid = bline[1:cut_slash]
        else:
            sid = bline.strip()
                
        seq = bytes(next(filename),
                    encoding='ascii').strip().upper()
        next(filename)
        quality = array("B",
                        bytes(next(filename),
                              encoding='ascii').strip())
        
        yield(sid,seq,quality)
                
