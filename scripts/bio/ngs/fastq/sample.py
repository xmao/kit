#!/usr/bin/env python
import sys,gzip,getopt
from Bio import SeqIO

try:
    opts,args = getopt.getopt(sys.argv[1:], 'n:')
except:
    raise
else:
    dopts = dict(opts)

by = int(dopts.get('-n', 2))

for f in args:
    total = 0
    print >> sys.stderr, f
    for s in SeqIO.parse(gzip.open(f), "fastq"):
        if total % by == 0:
            SeqIO.write(s, sys.stdout, "fastq")
        total = total + 1

