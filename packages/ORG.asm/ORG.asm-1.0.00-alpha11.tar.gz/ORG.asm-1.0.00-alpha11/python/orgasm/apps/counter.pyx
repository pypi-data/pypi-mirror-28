#cython: language_level=3

'''
Created on 27 mars 2016

@author: coissac
'''

import sys
from ..utils import bytes2str,str2bytes
from .config    cimport getConfiguration 
from builtins import None
from orgasm.utils import str2bytes


cdef class ProgressCounter:
    cdef clock_t clock(self):
        cdef clock_t t
        cdef timeval tp
        cdef clock_t s
        
        <void> gettimeofday(&tp,NULL)
        s = <clock_t> (<double> tp.tv_usec * 1.e-6 * <double> CLOCKS_PER_SEC)
        t = tp.tv_sec * CLOCKS_PER_SEC + s 
        
        return t

    def __init__(self,
                 off_t digits,
                 off_t logeach=10000,
                 dict  config={},
                 str head="",
                 str unit="",
                 double seconde=0.1):
        self.starttime = self.clock()
        self.lasttime  = self.starttime
        self.tickcount = <clock_t> (seconde * CLOCKS_PER_SEC)
        self.freq      = 1
        self.cycle     = 0
        self.lastlog   = 0
        self.logeach   = logeach 
        
        self.ontty = sys.stderr.isatty()
        
        self.digits = digits
        self._head = str2bytes(head)
        self.chead= self._head 
        
        self._unit = str2bytes(unit)
        self.cunit = self._unit
        
        try:
            if not config:
                config=getConfiguration()
        
            self.logger=config[config["__root_config__"]]["logger"]
        except RuntimeError:
            self.logger=None
                 
    def __call__(self,object pos):
        cdef off_t    ipos
        cdef clock_t  elapsed
        cdef clock_t  newtime
        cdef clock_t  delta
        cdef clock_t  more 
        cdef off_t    fraction
        cdef int      twentyth
        cdef double   speed
        
        self.cycle+=1
    
        if self.cycle % self.freq == 0:
            self.cycle=1
            newtime  = self.clock()
            delta         = newtime - self.lasttime
            self.lasttime = newtime
            elapsed       = newtime - self.starttime
#            print(" ",delta,elapsed,elapsed/CLOCKS_PER_SEC,self.tickcount)
            
            if   delta < self.tickcount / 5 :
                self.freq*=2
            elif delta > self.tickcount * 5 and self.freq>1:
                self.freq/=2
                
            
            if callable(pos):
                ipos=pos()
            else:
                ipos=pos
                
            if ipos==0:
                ipos=1                

            speed = ipos / <double>elapsed * CLOCKS_PER_SEC
                
            if self.ontty:
                    <void>fprintf(stderr,b'\r%s [%*d] speed : %*.1f %s/s',
                                    self.chead,
                                    self.digits,
                                    ipos,
                                    self.digits,
                                    speed,
                                    self.cunit)

            twentyth = int(ipos / self.logeach)
            if twentyth != self.lastlog and not self.ontty and self.logger is not None:
                self.logger.info('%s [%*d] speed : %*.1f %s/s' % (
                                        bytes2str(self._head),
                                        self.digits,
                                        ipos,
                                        self.digits,
                                        speed,
                                        bytes2str(self._unit)))
                self.lastlog=twentyth
        else:
            self.cycle+=1

    property head:
    
        def __get__(self):
            return self._head
        
        def __set__(self,str value):
            self._head=str2bytes(value)
            self.chead=self._head
