#!/usr/bin/env sh

xsv select cdr3s_aa,frequency,proportion $1 \
  | sed -e 1d -e s'/TRA:.*;TRB/TRB/' -e 's/TRB://' | grep -v 'TRA:' \
  | xsv fmt -t '\t' | sort | kit core nob -m sum | sort -k2,2nr
