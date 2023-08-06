#cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True

from cpython.array cimport array
from orgasm.apps.counter cimport ProgressCounter
from orgasm.backtranslate._ahocorasick cimport NucAhoCorasick,AhoCorasick

from docutils.nodes import line

from orgasm.files.universalopener import uopen
from ._fasta import readFasta
from ._fastq import readFastq

from zlib import compress,decompress
from pickle import dumps,loads

import sys
from orgasm.samples.phix import phix

__logger__ = None

cdef dict __stats__ = {}
cdef int  __interval__=50000

def logOrPrint(message,level='info'):
    global __logger__
    print(file=sys.stderr)
    if __logger__ is not None:
        getattr(__logger__, level)(message)
    else:
        print(message,file=sys.stderr)


cpdef tuple cut5prime(tuple sequence, int trimfirst=4):
    """
    Cuts the first *trimfirst* nucleotides of the sequence.
    The returned sequence can be empty
    """
    if len(sequence[1]) > trimfirst:
        return (sequence[0],
                sequence[1][trimfirst:],
                sequence[2][trimfirst:])
    else:
        return (sequence[0],
                b'',
                array("B",[]))
        
        
#cython: initializedcheck=False 
cdef int firstbelow(char[:] qualities, int quality, int shift=33):
    cdef int i =0
    cdef int lq=len(qualities)
    quality+=shift
    
    while(i < lq and qualities[i] >= quality):
        i+=1
        
    if i == lq:
        i=-1
        
    return i

cpdef tuple cut3primeQuality(tuple sequence, int quality, int shift=33):
    cdef int pos = firstbelow(sequence[2],quality,shift)
    
    if pos >= 0:
        return (sequence[0],
                sequence[1][0:pos],
                sequence[2][0:pos])
    else:
        return sequence
           
#cython: initializedcheck=False 
cpdef tuple longestACGT(bytes seq):
    cdef int maxLength = 0
    cdef int maxbegin  = 0
    cdef int maxend    = 0
    cdef int begin     = 0
    cdef int end       = 0
    cdef int length    = 0
    cdef int lseq = len(seq)
    cdef char* cseq = seq
    
    while (end < lseq):
        while (end < lseq and 
               ((cseq[end]==65) or   # A
                (cseq[end]==67) or   # C
                (cseq[end]==71) or   # G
                (cseq[end]==84))):   # T
            end+=1

        length = end - begin

        if length > maxLength:
            maxLength = length 
            maxbegin  = begin
            maxend    = end
        
        end+=1
        begin = end
        
    return (maxLength<lseq,maxbegin,maxend)

#cython: initializedcheck=False 
cpdef int bestWindow(char[:] qualities, int length):
    cdef int begin=-length
    cdef int end  = 0
    cdef int lseq = len(qualities)
    cdef int maxscore=0
    cdef int maxbegin=0
    cdef int cumscore=0
    
    if length >= lseq:
        return 0
        
    while (end < lseq):            
        cumscore+=qualities[end]
        
        if begin >=0:
            cumscore-=qualities[begin]
        
        begin+=1
        end+=1
        
        if begin > 0 and cumscore > maxscore:
            maxscore=cumscore
            maxbegin=begin 
        
    return maxbegin

#cython: initializedcheck=False 
cpdef tuple bestQuality(char[:] qualities, int quality, int shift=33):
    cdef int lseq = len(qualities)  # @DuplicatedSignature
    cdef int begin= 0
    cdef int end  = 0               # @DuplicatedSignature
    cdef int score= 0
    cdef int maxbegin
    cdef int maxend
    cdef int maxscore
     
    shift+=quality
    
    while (end < lseq):
        score+=qualities[end]-shift
        end+=1
        if score <= 0:
            begin = end
            score = 0
        if score >= maxscore:
            maxscore=score
            maxbegin=begin
            maxend  =end
     
    return (lseq > (maxend-maxbegin),maxbegin,maxend)       
    
            
def firstAndNextIterator(line,iterator):
    yield line
    
    for line in iterator:
        yield line
     
            
def PEInterleavedIterator(sequenceIterator):
    cdef tuple forward
    cdef int paircount=0
    
    logOrPrint("Decodes interleaved pair-end reads from a single file")

    for forward in sequenceIterator:
        paircount+=1
        yield (forward,next(sequenceIterator))

    __stats__['paircount']=paircount
        
def PESimulIterator(sequenceIterator):
    cdef tuple forward
    cdef array score 
    cdef int paircount=0
    
    logOrPrint("Simulating pair-end reads from single-end reads")

    
    for forward in sequenceIterator:
        score=array("B",forward[2])
        score.reverse()
        paircount+=1
        yield (forward,
               (forward[0],
                reverseComplement(forward[1]),
                score))

    __stats__['paircount']=paircount
     
def PEIterator(forwardIterator, reverseIterator):
    cdef tuple forward
    cdef int paircount=0

    logOrPrint("Two files pair-end data")

    
    for forward in forwardIterator:
        paircount+=1
        yield (forward,next(reverseIterator))
        
    __stats__['paircount']=paircount
        
def MPIterator(PEiterator):
    cdef tuple forward
    cdef tuple reverse
    
    logOrPrint("Analyze data as mate-pairs")

    for forward,reverse in PEiterator:
        forward[2].reverse()
        reverse[2].reverse()
        yield ((forward[0],
                reverseComplement(forward[1]),
                forward[2]),
               (reverse[0],
                reverseComplement(reverse[1]),
                reverse[2])
              )        
    
        
def PEIdCheckerIterator(PEiterator):
    cdef tuple PE
    cdef int   reject=0
    
    logOrPrint("Checking for badly paired sequence ids")
    
    for PE in PEiterator:
        if PE[0][0]==PE[1][0]:
            yield PE
        else:
            reject+=1
            if reject % __interval__ ==0:
                logOrPrint('%d sequence pairs with non corresponding ids' % reject)
                
    __stats__['bad_ids']=reject
        
   
def PECutter(PEiterator, int trimfirst=4):
    cdef tuple forward
    cdef tuple reverse
    
    logOrPrint("Hard clips the %d first base pairs of each read" % trimfirst)
    
    for forward,reverse in PEiterator:
        yield (cut5prime(forward,
                        trimfirst),
               cut5prime(reverse,
                        trimfirst))
        
def PEACGTCutter(PEiterator, int trimfirst=4):
    cdef tuple forward
    cdef tuple reverse
    cdef int   lf,lr,f,t
    cdef int trimmed=0
    
    logOrPrint("Select the longest region containing only [A,C,G,T]")

    for forward,reverse in PEiterator:
        lf,f,t  = longestACGT(forward[1])
        forward = (forward[0],
                   forward[1][f:t],
                   forward[2][f:t]) 
        
        lr,f,t  = longestACGT(reverse[1])
        reverse = (reverse[0],
                   reverse[1][f:t],
                   reverse[2][f:t]) 
        
        if lf or lr:
            trimmed+=1
            if not trimmed % __interval__:
                logOrPrint("%d sequences ACGT trimmed" % trimmed)
                
        yield (forward,reverse)
        
        __stats__["ACGTtrim"]=trimmed

def PELowQualityTrimmer(PEiterator, int quality, int shift=33): 
    cdef tuple forward
    cdef tuple reverse
    cdef int   lf,lr,f,t
    cdef int   trimmed=0
    
    logOrPrint("Soft clipping bad quality regions (below %d)." % quality)

    
    for forward,reverse in PEiterator:
        lf,f,t   = bestQuality(forward[2],quality,shift)
        if lf:
            forward = (forward[0],
                       forward[1][f:t],
                       forward[2][f:t]) 
        
        lr,f,t   = bestQuality(reverse[2],quality,shift)
        if lr : 
            reverse = (reverse[0],
                       reverse[1][f:t],
                       reverse[2][f:t]) 
            
        if lf or lr:
            trimmed+=1
            if not trimmed % __interval__:
                logOrPrint("%d sequences soft quality trimmed" % trimmed)
                

        yield (forward,reverse)
        __stats__["SoftQualityTrim"]=trimmed


def PEQualityTrimmer(PEiterator, int quality, int shift=33): 
    cdef tuple forward
    cdef tuple reverse
    
    logOrPrint("Hard clipping reads after the first base with a quality below %d." % quality)

    for forward,reverse in PEiterator:
        yield (cut3primeQuality(forward,
                               quality,
                               shift),
               cut3primeQuality(reverse,
                               quality,
                               shift))
        

#cython: initializedcheck=False 
def PELengthEstimate(PEiterator, double threshold=0.9,int minlength=81, bint zip=False):
    cdef tuple pair
    cdef tuple forward
    cdef tuple reverse
    cdef list  store = []
    cdef array histo = array('l',[0] * 1001)
    cdef long[:] chisto=histo
    cdef int   l,lf,lr
    cdef int   fb,rb
    cdef int   readcount
    cdef int   cumsum=0
    cdef int   lpair=0
    cdef int   lcut=1001 
    cdef int   counter=0
    cdef ProgressCounter pc = ProgressCounter(8,
                                              head="Read length estimate",
                                              seconde=0.5,
                                              unit="reads"
                                             )
    
    logOrPrint("Selecting the best length to keep %4.1f%% of the reads." % (threshold * 100))
    logOrPrint("   Minimum length set to %dbp" % minlength)
    
    for pair in  PEiterator:
        counter+=1
        pc(counter)
        lf = len(pair[0][1])
        lr = len(pair[1][1])
        l = lf if lf < lr else lr
        chisto[l]+=1
        
        if zip:
            store.append((l,compress(dumps(pair,protocol=3),9)))
        else:
            store.append((l,pair))
        
    readcount= sum(histo) *  threshold
    
    
    while (lcut >= 0 and cumsum < readcount):
        lcut-=1
        cumsum += chisto[lcut]
        
    print("",file=sys.stderr)
    logOrPrint("Indexing length estimated to : %dbp" % lcut)
    
    if lcut < minlength:
        lcut=minlength
        logOrPrint("Estimated length smaller than : %dbp" % minlength)
        logOrPrint("Indexing length reset to : %dbp" % lcut)

    for lpair,cpair in store:
        if lpair >= lcut:
            if zip:
                forward,reverse = loads(decompress(cpair))
            else:
                forward,reverse = cpair
            fb = bestWindow(forward[2],lcut)
            rb = bestWindow(reverse[2],lcut)

            yield  ((forward[0],
                     forward[1][fb:(fb+lcut)],
                     forward[2][fb:(fb+lcut)]),
                    (reverse[0],
                     reverse[1][rb:(rb+lcut)],
                     reverse[2][rb:(rb+lcut)]))
    

def PELengthCut(PEiterator, int length):
    cdef tuple forward
    cdef tuple reverse
    cdef int   fb,rb

    logOrPrint("Selecting the best subsequence of length %d." % length )

    for forward,reverse in  PEiterator:
        if len(forward[1]) >= length and len(reverse[1]) >= length :
            fb = bestWindow(forward[2],length)
            rb = bestWindow(reverse[2],length)
            
            yield  ((forward[0],
                     forward[1][fb:(fb+length)],
                     forward[2][fb:(fb+length)]),
                    (reverse[0],
                     reverse[1][rb:(rb+length)],
                     reverse[2][rb:(rb+length)]))

        

def PESkipFirstReads(PEI,int skip=0):
    cdef int n = 0
    
    logOrPrint("Skipping the %d first entries..." % skip)
    
    for n in range(skip):
        next(PEI)
        
    logOrPrint("Done.")

    return PEI

def PEMaxReadCount(PEI, int readCount):
    cdef int n 
    
    logOrPrint("Selecting %d good entries..." % readCount)

    for n in range(readCount):
        yield next(PEI)
    
#cython: initializedcheck=False
def PEPhiXCleaner(PEiterator):
    cdef tuple pair
    cdef char* forward
    cdef char* reverse
    cdef list fmatch,rmatch
    cdef int  nf,nr
    cdef int reject=0
    cdef AhoCorasick aho=NucAhoCorasick()
    aho.addSequence(phix["phi-X174"])
    aho.finalize()

    logOrPrint("Sorting out PhiX174 read pairs..." )
    
    for pair in PEiterator:
        forward = pair[0][1]
        reverse = pair[1][1]
        nf=(len(forward)-11) * 2 // 3
        nr=(len(reverse)-11) * 2 // 3
        
        fmatch=aho.match(forward)
        rmatch=aho.match(reverse)
        
        if (len(fmatch[1]) >= nf or len(fmatch[2]) >= nf or
            len(rmatch[1]) >= nr or len(rmatch[2]) >= nr):
            reject+=1
            if reject % __interval__ ==0:
                logOrPrint('%d phiX174 sequence pairs rejected' % reject)
        else:
            yield pair 
    __stats__['phix174']=reject
            

def readSequences(filename):
    
    if isinstance(filename, str):
        filename = uopen(filename)
    
    firstline = next(filename)
    li = firstAndNextIterator(firstline,filename)
    if firstline[0]==">":
        return readFasta(li)
    else:
        return readFastq(li)

def readPairedEnd(filenames,
                  str     mode="PE",
                  bint    checkIds=False,
                  int     cut=4,
                  int     badQualityLimit=28,
                  int     qualityCut=0,
                  int     length=0,
                  double  lengthestimate=0.9,
                  int     minlength=81,
                  int     skip=0,
                  int     maxread=0,
                  bint    phix=True,
                  int     shift=33,
                  bint    zip=False
                  ):
        
    PEI = None
    
    if mode=="MP":
        matepair=True
        mode="PE"
    elif mode=="IMP":
        matepair=True
        mode="IPE"
    else:
        matepair=False
    
    if mode=='PE' and len(filenames) > 1:
        forward = readSequences(filenames[0])
        reverse = readSequences(filenames[1])
        PEI = PEIterator(forward,reverse)
    
    if mode=='SimPE':
        PEI = PESimulIterator(filenames[0])
    
    if mode=='IPE' or (mode=='PE' and len(filenames)==0):
        PEI = PEInterleavedIterator(filenames[0])
        
    if PEI is not None :
        
        if skip > 0:
            PEI = PESkipFirstReads(PEI,skip)
            
        if checkIds:
            PEI = PEIdCheckerIterator(PEI)
        
        if cut > 0:
            PEI = PECutter(PEI,cut)
            
        PEI = PEACGTCutter(PEI)
            
        if badQualityLimit > 0:
            PEI = PELowQualityTrimmer(PEI,badQualityLimit,shift)
            
        if qualityCut > 0:
            PEI = PEQualityTrimmer(PEI,qualityCut,shift)
                    
        if phix:
            PEI = PEPhiXCleaner(PEI)
            
        if length>0 :
            PEI = PELengthCut(PEI,length)
        elif lengthestimate > 0:
            PEI = PELengthEstimate(PEI,lengthestimate,minlength,zip)
            
        if maxread > 0:
            PEI = PEMaxReadCount(PEI,maxread)
            
        if matepair:
            PEI = MPIterator(PEI)
        
        return PEI
    
    raise AttributeError('Cannot find suitable sequence file names')
    
    
cpdef dict getStats():
    return __stats__

cpdef setLogger(logger):
    global __logger__
    __logger__=logger
    