#cython: language_level=3
from cpython.array cimport array
from orgasm.files.universalopener import uopen


def readFasta(filename,int quality=40,int shift=33):
    
    cdef int   seqid = 0
    cdef int   cut_slash
    cdef int   cut_space
    
    cdef bytes seq
    cdef list  seqlines = []
    
    if isinstance(filename, str):
        filename = uopen(filename)
    
    try:        
        line  = next(filename) 
        bline = bytes(line,
                      encoding='ascii'
                     )

        while(bline[0]!=62):   # ord(b'>')
            bline = bytes(next(filename),
                          encoding='ascii'
                         )

        while(1):
                            
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
                
            bline = bytes(next(filename),
                          encoding='ascii'
                         )
                
            while (bline[0]!=62):   # ord(b'>')
                seqlines.append(bline.strip().upper())
                
                bline = bytes(next(filename),
                              encoding='ascii'
                             )
                
            seq = b''.join(seqlines)
            yield (sid,
                   seq,
                   array('B',[quality+shift] * len(seq)))
            seqlines=[]
                
    except StopIteration:
        pass
    
    seq = b''.join(seqlines)
    yield (sid,
           seq,
           array('B',[quality+shift] * len(seq)))

                    
