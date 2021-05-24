#!/scratch/rists/hpcapps/rhel6/python/anaconda/bin/python
import sys

import pysam                              # >=0.8.1
from Bio import SeqIO

def get_input_stream(file, type_):
    if type_ in ('sam', 'bam'):
        if type_ == 'sam':
            return pysam.AlignmentFile(file, 'r')
        else:
            return pysam.AlignmentFile(file, 'rb')
    elif type_ in ('fastq', ):
        return SeqIO.parse(file, 'fastq')
    elif type_ in ('txt', ):
        return open('file', 'r')
    else:
        print >> sys.stderr, 'Unsupported file type: %s' % type_
        sys.exit(1)

def get_scalable_dbm(file, backend='memory', **kargs):
    if backend == 'memory':
        return {}
    elif backend == 'dbm':
        if sys.version_info.major < 3:
            import anydbm
            return anydbm.open(file, 'c', **kargs)
        else:
            import dbm
            return dbm.open(file, 'c', **kargs)
    elif backend == 'sqlite':
        import sqlite_dbm
        return sqlite_dbm.open(file, **kargs)
    elif backend == 'bsddb3':
        import bsddb3
        return bsddb3.btopen(file, cachesize=(2 * 1024**3 - 1)) # 1Gb cache size
    else:
        print >> sys.stderr, 'Unsupported dbm backend: %s' % backend
        sys.exit(1)

def usage():
    return '%s -d memory|bsddb3|dbm|sqlite -a FilterBAM -b BAMOrFastqToBeFiltered' % sys.argv[0]

if __name__ == '__main__':
    import os,sys,getopt
    import datetime
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:b:d:')
    except:
        raise
    else:
        dopts = dict(opts)

    if len(dopts) < 1 or '-a' not in dopts or '-b' not in dopts:
        print >>sys.stderr, usage()
        sys.exit(1)
    
    dbfile = '%s.%s' % (os.path.splitext(dopts['-a'])[0], dopts.get('-d', 'memory'))
    if dopts.get('-d') == 'memory' or (not os.path.isfile(dbfile)):
        db = get_scalable_dbm(dbfile, backend=dopts.get('-d', 'memory'))
        print >>sys.stderr, 'Starting caching IDs into %s on %s' % (
            dopts.get('-d', 'memory'),
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
        input1 = get_input_stream(
            dopts['-a'], os.path.splitext(dopts['-a'])[1][1:])
        
        count = 0
        for i in input1:
            if not i.is_unmapped:
                db[i.qname] = '1'
                count += 1
        
        print >>sys.stderr, "%d mapped reads are cached." % count
    else:
        db = get_scalable_dbm(dbfile, backend=dopts.get('-d', 'dbm'))
        print >>sys.stderr, 'Using existed hash table from %s' % dbfile

    print >>sys.stderr, 'Filtering all IDs on %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count = 0
    inext2 = os.path.splitext(dopts['-b'])[1][1:]
    input2 = get_input_stream(dopts['-b'], inext2)
    if inext2 == 'bam':
        outfile2 = pysam.AlignmentFile('-', 'wh', template=input2)
        for i in input2:
            if i.qname not in db:
                outfile2.write(i)
            else:
                count += 1
    else:
        for i in input2:
            if i.id[:-2] not in db:
                print i.format('fastq'),
            else:
                count += 1
    print >>sys.stderr, 'Done on %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print >>sys.stderr, '%d reads are filtered out' % count
    
    if dopts.get('-d', 'memory') != 'memory':
        db.close()
