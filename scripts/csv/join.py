#!/usr/bin/env python

import argparse


def get_argument_parser():
    parser = argparse.ArgumentParser(description = "join multiple files based on key columns")
    parser.add_argument('files', nargs = '+', help = 'two or more csv files')
    parser.add_argument('-k', '--keys', default = 'key', help = 'one or more key columns')
    parser.add_argument('-v', '--values', default = 'value', help = 'one or more key columns')
    parser.add_argument('-n', '--names', help = 'mapping table between files and names')

    return parser


if __name__ == '__main__':
    import os,sys,csv
    import collections

    parser = get_argument_parser()
    args = parser.parse_args()

    key_cols = args.keys.split(',')
    val_cols = args.values.split(',')
    
    if args.names:
        name_map = dict([ i.strip().split()[:2] for i in open(args.names) ])
    else:
        name_map = dict([ (os.path.basename(args.files[i]), i+1) for i in range(len(args.files))  ])

    header, files = [], collections.OrderedDict()
    header.extend(key_cols)
    for f in args.files:
        n = name_map[os.path.basename(f)]
        header.extend(['{}.{}'.format(n, v) for v in val_cols])

        files[n] = {}
        for row in csv.DictReader(open(f), dialect="excel-tab"):
            k = ':'.join([ row[i] for i in key_cols ])
            files[n][k] = [ row[i] for i in val_cols ]

    keys = set()
    for f in files.values():
        keys.update(f.keys())

    print '\t'.join(header)

    for k in keys:
        print '{}\t{}'.format(
            '\t'.join(k.split(':')),
            '\t'.join([ '\t'.join(f.get(k, "")) for f in files.values() ])
        )
