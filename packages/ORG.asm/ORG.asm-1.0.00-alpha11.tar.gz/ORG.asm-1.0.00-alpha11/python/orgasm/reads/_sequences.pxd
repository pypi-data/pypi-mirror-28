from orgasm.utils.dna cimport reverseComplement

cpdef tuple cut5prime(tuple sequence, int trimfirst=?)
cdef int firstbelow(char[:] qualities, int quality, int shift=?)
cpdef tuple cut3primeQuality(tuple sequence, int quality, int shift=?)
cpdef tuple longestACGT(bytes seq)
cpdef int bestWindow(char[:] qualities, int length)
cpdef dict getStats()
