# cython: language_level=3

from orgasm.tango import pairEndedConnected
from orgasm.tango import estimateFragmentLength
from orgasm.tango import logOrPrint

from orgasm.utils import bytes2str


def buildReadSequence(self,assgraph,identifier,path,back=200,nlength=20,logger=None):
    
    #
    # Build a dictionary with:
    #      - Keys   = stemid
    #      - Values = edge descriptor (from,to,x)
    #
    readsize = self.index.getReadSize()
    frglen,frglensd = estimateFragmentLength(self) # @UnusedVariable
    
    alledges = dict((assgraph.getEdgeAttr(*e)['stemid'],e) 
                    for e in assgraph.edgeIterator(edgePredicate = lambda i: 'stemid' in assgraph.getEdgeAttr(*i)))

    seq=[]
    oldstem=None
    oldid=None
    oldstemclass=None
     
    rank = 1
    forceconnection=False
    
    for stemid in path:
        if stemid != 0:
            stem              = alledges[stemid]
            attr              = assgraph.getEdgeAttr(*stem)
            stemclass         = attr['class']
            sequence          = attr['path']
            
            if rank==1 and stemclass!="sequence":
                raise RuntimeError("A path cannot start on a gap")

                                                    # Switch the stem to a dashed style
            graphics          = attr.get('graphics',{})
            attr['graphics']  = graphics
            graphics['style'] = 'dashed'
            
            # Manage step rank information of each step
            allsteps = attr.get('steps',{})
            steps = allsteps.get(identifier,[])
            steps.append(rank)
            allsteps[identifier]=steps
            attr['steps']=allsteps
            
            if oldstem is not None:
                connected,ml,sl,delta = pairEndedConnected(self,assgraph,oldid,stemid,back)  # @UnusedVariable
                if oldstem[1]==stem[0]:
                    if oldstemclass=="sequence":
                        if stemclass=="sequence":                   # Link between 2 sequences
                            if ml is not None:
                                logOrPrint(logger,
                                           "Both segments %d and %d are connected (paired-end=%d frg length=%f sd=%f)" % 
                                           (oldid,stemid,connected,float(ml),float(sl)))
            
                            else:
                                logOrPrint(logger,
                                           "Both segments %d and %d are connected but covered by 0 paired-end" % 
                                           (oldid,stemid))
            
                                                            
                        elif stemclass[0:9]=="scaffold:":           # Link a sequence and a gap
                            logOrPrint(logger,
                                        "Both segments %d and %d are disconnected" % attr['link'])
    
                            if stemclass=="scaffold:paired-end":
                                logOrPrint(logger,
                                           "   But linked by %d pair ended links (gap length=%f sd=%f)" % 
                                           (attr['pairendlink'],
                                            attr['length'],
                                            attr['gapsd']))
                                           
    
                            elif stemclass=="scaffold:forced":
                                logOrPrint(logger,"   Connection is forced")
                                
                                if attr['pairendlink'] > 0:
                                    logOrPrint(logger,
                                               "   But asserted by %d pair ended links (gap length=%f sd=%f)" % 
                                               (attr['pairendlink'],
                                                attr['length'],
                                                attr['gapsd']))
                            elif stemclass=="scaffold:overlap":
                                logOrPrint(logger,
                                           "   But overlap by %dbp supported by %d pair ended links" % 
                                           (-attr['length'],
                                            attr['pairendlink']))
                                        
                    elif oldstemclass[0:9]=="scaffold:" and stemclass[0:9]=="scaffold:":
                        raise RuntimeError('A scaffold link must be followed by a sequence %d --> %d' %
                                           (oldid,stemid))           
                        
                elif forceconnection:
                    logOrPrint(logger,"   Connection is forced")
                    if connected > 0:
                        glength = int(frglen-ml - readsize) 

                        logOrPrint(logger,
                                   "   But asserted by %d pair ended links (gap length=%f sd=%f)" % 
                                   (connected,
                                    glength,
                                    sl))

                    else:
                        
                        logOrPrint(logger,
                                   "Without any support from pair ended links")
                        glength =  nlength
                    
                    seq.append([0] * int(glength) + [stem[0]])

                    # Add the foced link to the compact assembly graph    
                    flink = assgraph.addEdge(oldstem[1],stem[0])
                    rlink = assgraph.addEdge(-stem[0],-oldstem[1])
                    flink['label']="Forced (%d)  %d -> %d" % (connected,oldid,stemid)
                    flink['graphics']={'width':1,
                                       'arrow':'last',
                                       'fill':'0xFF0000',
                                       'style':'dashed'

                                      }
                    rlink['label']="Forced (%d)  %d -> %d" % (connected,-stemid,-oldid)
                    rlink['graphics']={'width':1,
                                       'arrow':'last',
                                       'fill':'0xFF0000',
                                       'style':'dashed'
                                      }
                else:
                    raise AssertionError('Disconnected path between stem '
                                         '%d and %d only %d pair ended links' % (oldid,stemid,connected))



            if stemclass=="sequence":
                if attr['length'] > 10:
                    attr['label']="%d : %s->(%d)->%s  [%d] @ %s" % (stemid,attr['sequence'][0:5].decode('ascii'),
                                                                    attr['length'],
                                                                    attr['sequence'][-5:].decode('ascii'),
                                                                    int(attr['weight']),
                                                                    attr['steps'])
                else:
                    attr['label']="%d : %s->(%d)  [%d] @ %s" % (stemid,
                                                                attr['sequence'].decode('ascii'),
                                                                attr['length'],
                                                                int(attr['weight']),
                                                                attr['steps'])
                    
 #           if oldstemclass is not None:
            if seq:
                seq.append(sequence[1:])
            else:
                seq.append(sequence)

            rank+=1
            oldstem = stem
            oldid=stemid
            oldstemclass=stemclass
            
            forceconnection=False
        else:
            forceconnection=True

    
                        
            
        
    s1 = alledges[path[-1]]
    s2 = alledges[path[0]]
    sid1=assgraph.getEdgeAttr(*s1)['stemid']
    sid2=assgraph.getEdgeAttr(*s2)['stemid']
    sclass2=assgraph.getEdgeAttr(*s2)['class']
    connected,ml,sl,delta = pairEndedConnected(self,            # @UnusedVariable
                                               assgraph,
                                               sid1,
                                               sid2,
                                               back)  
    
    if s1[1]==s2[0]:
        logOrPrint(logger, "Path is circular")
                    
            
        circular=True
        seq[-1].pop()
    else:
        if sclass2!="sequence":
            raise RuntimeError("A path cannot ends on a gap")
        
        if forceconnection:
            logOrPrint(logger,"Circular connection forced",)
            logOrPrint(logger,"Linked by %d pair ended links" %  connected)
                
            seq.append([0]*int(nlength))
            circular=True
        else:
            logOrPrint(logger,"Path is linear")
            circular=False

#        seq.insert(0,self.index.getRead(s2[0],0,self.index.getReadSize()).lower())

    sequence=[]
    for l in seq:
        sequence.extend(l)
         
    readsize=self.index.getReadSize()
        
    if circular:
        sequence = sequence[readsize:] + sequence[0:readsize]
         
    
    return sequence

def path2sam(self,assgraph,path,identifier="contig",minlink=10,nlength=20,back=200,logger=None,tags=[]):
    '''
    Convert a path in an compact assembling graph in a fasta formated sequences.
    
    :param assgraph: The compact assembling graph as produced by the
                     :py:meth:`~orgasm.assembler.Assembler.compactAssembling` method
    :type assgraph:  :py:class:`~orgasm.graph.DiGraphMultiEdge`
    :param path:     an ``iterable`` providing an ordered list of ``stemid`` indicating
                     the path to follow.  
    :type path:      an ``iterable`` over :py:class:`int`
    :param identifier: the identifier used in the header of the fasta formated sequence
    :type identifier:  :py:class:`bytes`
    :param minlink:  the minimum count of pair ended link to consider 
                     for asserting the relationship
    :type minlink:   :py:class:`int`
    :param nlength:  how many ``N`` must be added between two segment of sequences only connected
                     by pair ended links
    :type nlength:   :py:class:`int`
    :param back:     How many base pairs must be considered at the end of each edge
    :type back:      :py:class:`int`
    
    :returns: a string containing the fasta formated sequence
    :rtype: :py:class:`bytes`

    :raises: :py:class:`AssertionError`
    '''
    
    readsize = self.index.getReadSize()
#    frglen,frglensd = estimateFragmentLength(self) # @UnusedVariable
        
    sequence = buildReadSequence(self,assgraph,identifier,path,back,nlength,logger)
#     seq=[]
#     oldstem=None
#     oldid=None
#     oldstemclass=None
#      
#     rank = 1
#     forceconnection=False
#     
#     for stemid in path:
#         if stemid != 0:
#             stem              = alledges[stemid]
#             attr              = assgraph.getEdgeAttr(*stem)
#             stemclass         = attr['class']
#             sequence          = attr['path']
#             
#             if rank==1 and stemclass!="sequence":
#                 raise RuntimeError("A path cannot start on a gap")
# 
#                                                     # Switch the stem to a dashed style
#             graphics          = attr.get('graphics',{})
#             attr['graphics']  = graphics
#             graphics['style'] = 'dashed'
#             
#             # Manage step rank information of each step
#             allsteps = attr.get('steps',{})
#             steps = allsteps.get(identifier,[])
#             steps.append(rank)
#             allsteps[identifier]=steps
#             attr['steps']=allsteps
#             
#             if oldstem is not None:
#                 connected,ml,sl,delta = pairEndedConnected(self,assgraph,oldid,stemid,back)  # @UnusedVariable
#                 if oldstem[1]==stem[0]:
#                     if oldstemclass=="sequence":
#                         if stemclass=="sequence":                   # Link between 2 sequences
#                             if ml is not None:
#                                 logOrPrint(logger,
#                                            "Both segments %d and %d are connected (paired-end=%d frg length=%f sd=%f)" % 
#                                            (oldid,stemid,connected,float(ml),float(sl)))
#             
#                             else:
#                                 logOrPrint(logger,
#                                            "Both segments %d and %d are connected but covered by 0 paired-end" % 
#                                            (oldid,stemid))
#             
#                                                             
#                         elif stemclass[0:9]=="scaffold:":           # Link a sequence and a gap
#                             logOrPrint(logger,
#                                         "Both segments %d and %d are disconnected" % attr['link'])
#     
#                             if stemclass=="scaffold:paired-end":
#                                 logOrPrint(logger,
#                                            "   But linked by %d pair ended links (gap length=%f sd=%f)" % 
#                                            (attr['pairendlink'],
#                                             attr['length'],
#                                             attr['gapsd']))
#                                            
#     
#                             elif stemclass=="scaffold:forced":
#                                 logOrPrint(logger,"   Connection is forced")
#                                 
#                                 if attr['pairendlink'] > 0:
#                                     logOrPrint(logger,
#                                                "   But asserted by %d pair ended links (gap length=%f sd=%f)" % 
#                                                (attr['pairendlink'],
#                                                 attr['length'],
#                                                 attr['gapsd']))
#                             elif stemclass=="scaffold:overlap":
#                                 logOrPrint(logger,
#                                            "   But overlap by %dbp supported by %d pair ended links" % 
#                                            (-attr['length'],
#                                             attr['pairendlink']))
#                                         
#                     elif oldstemclass[0:9]=="scaffold:" and stemclass[0:9]=="scaffold:":
#                         raise RuntimeError('A scaffold link must be followed by a sequence %d --> %d' %
#                                            (oldid,stemid))           
#                         
#                 elif forceconnection:
#                     logOrPrint(logger,"   Connection is forced")
#                     if connected > 0:
#                         glength = int(frglen-ml - self.index.getReadSize()) 
# 
#                         logOrPrint(logger,
#                                    "   But asserted by %d pair ended links (gap length=%f sd=%f)" % 
#                                    (connected,
#                                     glength,
#                                     sl))
# 
#                     else:
#                         
#                         logOrPrint(logger,
#                                    "Without any support from pair ended links")
#                         glength =  nlength
#                     
#                     seq.append([0] * int(glength) + [stem[0]])
# 
#                     # Add the foced link to the compact assembly graph    
#                     flink = assgraph.addEdge(oldstem[1],stem[0])
#                     rlink = assgraph.addEdge(-stem[0],-oldstem[1])
#                     flink['label']="Forced (%d)  %d -> %d" % (connected,oldid,stemid)
#                     flink['graphics']={'width':1,
#                                        'arrow':'last',
#                                        'fill':'0xFF0000',
#                                        'style':'dashed'
# 
#                                       }
#                     rlink['label']="Forced (%d)  %d -> %d" % (connected,-stemid,-oldid)
#                     rlink['graphics']={'width':1,
#                                        'arrow':'last',
#                                        'fill':'0xFF0000',
#                                        'style':'dashed'
#                                       }
#                 else:
#                     raise AssertionError('Disconnected path between stem '
#                                          '%d and %d only %d pair ended links' % (oldid,stemid,connected))
# 
# 
# 
#             if stemclass=="sequence":
#                 if attr['length'] > 10:
#                     attr['label']="%d : %s->(%d)->%s  [%d] @ %s" % (stemid,attr['sequence'][0:5].decode('ascii'),
#                                                                     attr['length'],
#                                                                     attr['sequence'][-5:].decode('ascii'),
#                                                                     int(attr['weight']),
#                                                                     attr['steps'])
#                 else:
#                     attr['label']="%d : %s->(%d)  [%d] @ %s" % (stemid,
#                                                                 attr['sequence'].decode('ascii'),
#                                                                 attr['length'],
#                                                                 int(attr['weight']),
#                                                                 attr['steps'])
#                     
#  #           if oldstemclass is not None:
#             if seq:
#                 seq.append(sequence[1:])
#             else:
#                 seq.append(sequence)
# 
#             rank+=1
#             oldstem = stem
#             oldid=stemid
#             oldstemclass=stemclass
#             
#             forceconnection=False
#         else:
#             forceconnection=True
# 
#     
#                         
#             
#         
#     s1 = alledges[path[-1]]
#     s2 = alledges[path[0]]
#     sid1=assgraph.getEdgeAttr(*s1)['stemid']
#     sid2=assgraph.getEdgeAttr(*s2)['stemid']
#     sclass2=assgraph.getEdgeAttr(*s2)['class']
#     connected,ml,sl,delta = pairEndedConnected(self,            # @UnusedVariable
#                                                assgraph,
#                                                sid1,
#                                                sid2,
#                                                back)  
#     
#     if s1[1]==s2[0]:
#         logOrPrint(logger, "Path is circular")
#                     
#             
#         circular=True
#         seq[-1].pop()
#     else:
#         if sclass2!="sequence":
#             raise RuntimeError("A path cannot ends on a gap")
#         
#         if forceconnection:
#             logOrPrint(logger,"Circular connection forced",)
#             logOrPrint(logger,"Linked by %d pair ended links" %  connected)
#                 
#             seq.append([0]*int(nlength))
#             circular=True
#         else:
#             logOrPrint(logger,"Path is linear")
#             circular=False
# 
# #        seq.insert(0,self.index.getRead(s2[0],0,self.index.getReadSize()).lower())
# 
#     sequence=[]
#     for l in seq:
#         sequence.extend(l)
#          
#     readsize=self.index.getReadSize()
#         
#     if circular:
#         sequence = sequence[readsize:] + sequence[0:readsize]
#          
#         
    reads = []
    location={}
    
    
    for i in range(len(sequence)):
        rid = sequence[i]
        rl={}
        reads.append(rl)       
#        if rid !=0 and not self.index.isFake(rid):
        if rid !=0:
            fake = self.index.isFake(rid)
            if not fake:
                allreads = self.index.getIds(rid)
                signe = 1 if rid > 0 else -1
                for rid in allreads[2]:
                    rid*=signe
                    prid = self.index.getPairedRead(rid)
                    rl[rid]=(prid,min(abs(rid),abs(prid)))
                    if rid not in location:
                        lp=[]
                        location[rid]=lp
                    else:
                        lp=location[rid]
                    lp.append(i+1)
            else:
                rl[rid]=(None,None)
                if rid not in location:
                    lp=[]
                    location[rid]=lp
                else:
                    lp=location[rid]
                lp.append(i+1)
                     
    sam=[]
    mapped=set()
    
    nreads = len(reads)
    
    def distreads(rid,a,b):
        if rid > 0:
            d = b - a + 1
        else:
            d = a - b
        if d < 0:
            d+=nreads
        return d
        
    
    for i in range(nreads):
        rlist=reads[i]
        for rid in rlist:
            flag=0
            
            paired,qname=rlist[rid]
            if paired is not None:
                npaired= self.index.getIds(paired)[0]

                paired_mapped = npaired in location
                flag |= 0x01            # template having multiple segments in sequencing
                                        # All our reads are paired   
                                        
                mapping=255  
                optional=""                   
    
            else:
                paired_mapped = False
                mapping=0
                optional="fk:i:1"
                
                
            readpos=i+1
            
            if paired_mapped:
                dist = [distreads(rid,readpos,x)
                        for x in location[npaired]]
                pairedpos=location[npaired][dist.index(min(dist))]
                if readpos < pairedpos:
                    tlen = pairedpos - readpos + readsize
                else:
                    tlen = -(readpos - pairedpos + readsize)
            else:
                qname = abs(rid)
                pairedpos=0
                tlen=0

            if paired_mapped:
                flag |= 0x02        # each segment properly aligned according to the aligner
                                    # paired read is part of the assembly        
                if rid > 0:      
                    flag |= 0x40    # the first segment in the template
                    flag |= 0x20    # SEQ of the next segment in the template being reverse complemented
                else:
                    flag |= 0x80    # the last segment in the template
            else:
                flag |= 0x08        # next segment in the template unmapped
                    
            
            if rid < 0:
                flag |= 0x10        # SEQ being reverse complemented
                
            if abs(rid) in mapped:
                flag|=0x100         # secondary alignment
            else:
                mapped.add(abs(rid))
                
            rseq = bytes2str(self.index.getRead(rid,
                                          0,
                                          self.index.getReadSize()).upper())
                 
            sam.append("R%09d\t%d\t%s\t%d\t%d\t%dM\t%s\t%d\t%d\t%s\t*" 
                                                % (qname,
                                                   flag,identifier,          
                                                   readpos,                           # Read position
                                                   mapping,                               # No mapping quality
                                                   readsize,                          # For the CIGAR string
                                                   '=' if paired_mapped else '*',     # 
                                                   pairedpos,
                                                   tlen,
                                                   rseq
                                                   ))
            
            if len(optional):
                sam[-1]=sam[-1]+ "\t" + optional
                
#    print(sequence[0:20])
#    print(reads[0:20])

    #sequence = b''.join(seq)
    #length = len(sequence)
    
    sam = "\n".join(sam)
    
    return sam
