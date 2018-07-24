#!/usr/bin/env python

import os, collections

from csvkit import CSVKitReader, CSVKitWriter
from csvkit.cli import CSVKitUtility, parse_column_identifiers
from csvkit.headers import make_default_headers

class CSVIntersect(CSVKitUtility):
    description = 'Intersect the key rows for multiple CSV files.'
    override_flags = ['f']

    def add_arguments(self):
        self.argparser.add_argument(metavar="FILE", nargs='+', dest='input_paths', default=['-'],
            help='The CSV file(s) to operate on. If omitted, will accept input on STDIN.')
        self.argparser.add_argument('-c', '--columns', dest='columns',
            help='A comma separated list of column indices or names to be examined. Defaults to all columns.')

    def parse_column_identifiers(self, floc, *args):
        columns = []
        for i in self.args.columns.split(','):
            if i.find('|') != -1:
                columns.append(i.split('|')[floc])
            else:
                columns.append(i)
        return parse_column_identifiers(','.join(columns), *args)

    def main(self):
        self.input_files = []

        for path in self.args.input_paths:
            self.input_files.append(self._open_input_file(path))

        if len(self.input_files) < 2:
            self.argparser.error('You must specify at least two files to intersect.')


        intersection = collections.OrderedDict()
        output = CSVKitWriter(self.output_file, **self.writer_kwargs)
        
        for i, f in enumerate(self.input_files):
            rows = CSVKitReader(f, **self.reader_kwargs)
            column_indices = self.parse_column_identifiers(i, next(rows), self.args.zero_based)

            for row in rows:
                # import pdb; pdb.set_trace()
                key = ':'.join([ row[j] for j in column_indices ])
                if key not in intersection:
                    intersection[key] = [ 0 for j in range(len(self.input_files)) ]
                intersection[key][i] = 1

        output.writerow(['Key'] + [
            os.path.splitext(os.path.basename(i))[0] for i in self.args.input_paths ])

        for k,v in intersection.items():
            output.writerow([k] + [ str(j) for j in v ])
    
def launch_new_instance():
    utility = CSVIntersect()
    utility.main()
    
if __name__ == "__main__":
    launch_new_instance()
