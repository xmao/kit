#!/usr/bin/env sh

set -e

for i in */outs/clonotypes.csv; do
    kit 10X get_trb.sh $i | xsv fmt -d '\t' > $(dirname $i | xargs -n 1 dirname)-TRB.csv
done
