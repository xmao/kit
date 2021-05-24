#!/usr/bin/env bash

COUNT=10

while getopts :n: OPT; do
    case $OPT in
        n|+n)
            COUNT="$OPTARG"
            ;;
        *)
            echo "usage: `basename $0` [+-n ARG} [--] ARGS..."
            exit 2
    esac
done
shift `expr $OPTIND - 1`
OPTIND=1


comm -1 -2 \
    <(head -n $(($COUNT+1)) $1 | xsv select cdr3s_aa | sed -e 1d -e s'/TRA:.*;TRB/TRB/' | sort) \
    <(head -n $(($COUNT+1)) $2 | xsv select cdr3s_aa | sed -e 1d -e s'/TRA:.*;TRB/TRB/' | sort)

