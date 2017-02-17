#!/usr/bin/env python

import sys,csv,re,getopt

def get_mapping_by_alternate_key(mapping, keys):
    for k in keys:
        if k in mapping:
            return mapping[k]

try:
    opts, args = getopt.getopt(sys.argv[1:], ':d:m:k:n:')
except:
    raise
else:
    dopts = dict(opts)

d = {}
for i in open(dopts['-m']):
    ii = re.split(dopts.get('-d', r'\s'), i)
    if len(ii) >= 2:
        d[ii[0]] = ii[1]

keys = [ int(i)-1 for i in dopts.get('-k', '1').split(',') ]
n = dopts.get('-n', 'mapped')

print '%s\t%s' % (sys.stdin.next().rstrip(), n)

for i in csv.reader(sys.stdin, dialect='excel-tab'):
    print '%s\t%s' % ('\t'.join(i), get_mapping_by_alternate_key(d, [ i[k] for k in keys ] ))

