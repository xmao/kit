#!/usr/bin/env python3

import sys
from Bio import SeqIO

for r in SeqIO.parse(sys.argv[1], "fasta"):
    print("{}\t{}".format(r.id, len(r.seq)))
