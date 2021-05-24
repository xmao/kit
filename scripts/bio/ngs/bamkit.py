#!/usr/bin/env python

import pysam # >= 0.8.1

def bam_diff(file1, file2):
    set1, set2 = set(), set()
    
    for i in pysam.AlignmentFile(file1, 'rb'):
        if not i.is_unmapped:
            set1.add(i.qname)

    for i in pysam.AlignmentFile(file2, 'rb'): 
        if not i.is_unmapped:
            set2.add(i.qname)

    n1 = len(set1.difference(set2))
    n2 = len(set1.intersection(set2))
    n3 = len(set2.difference(set1))

    return (n1, n2, n3)

def bam_id(f, is_mapped=None):
    for i in pysam.AlignmentFile(f, 'rb'):
        if is_mapped:
            if not i.is_unmapped:
                print i.qname
        else:
            print i.qname

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) <= 1:
        print >>sys.stderr, '%s diff|... [options]' % sys.argv[0]
        sys.exit(1)
    
    func = globals().get('bam_%s' % sys.argv[1])
    if func:
        print func(*sys.argv[2:])
    else:
        print >>sys.stderr, 'Not supported function: %s' % sys.argv[1]
        sys.exit(1)
