#!/usr/bin/env bash

REFFA=${REFFA:-/scratch/rists/hpcapps/reference/human/hg19/indexes/hg19BWA0.7.5aIndex/Homo_sapiens_assembly19.fasta}
GTF=${GTF:-/scratch/rists/hpcapps/reference/human/hg19/annotations/ensemble/Homo_sapiens.GRCh37.75.gtf}
GTFBED=${GTFBED:-}

function getFastaFromReference {
    bedtools getfasta -fi $REFFA -bed $1 -fo -
}

function getGeneForBed {
    bedmap --echo --echo-map --range 100 --delim '\t' $1 $GTFBED
}

function doConvertGTF {
    cat ${GTF} | gtf2bed --do-not-sort | awk -F '\t' -v type=${1:-gene} '{ if($8 == type) print $0; }'
}

function doConvertOneToZeroBase {
    awk '{ printf("%s\i\t%i\n", $1, $2-1, $3); }'
}

function help {
    printf "%s %s [options] \n" "$(basename $0)" "$(typeset -f | grep -e '^do' -e '^get' | sed -e 's/ .*//' | tr '\n' '|' | sed -e 's/|$//')"
}

CMD=$1; shift 1

case $CMD in
    g|fa|getFastaFromReference)
        getFastaFromReference $*
        ;;
    c|gtf|doConvertGTF)
        doConvertGTF $*
        ;;
    *)
        help
esac
