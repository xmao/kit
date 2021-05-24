#!/usr/bin/env sh

set -ex

MODE="link"
while getopts :m OPT; do
    case $OPT in
        m|+m)
            MODE="$OPTARG"
            ;;
        *)
            echo "usage: `basename $0` [+-m} [--] ARGS..."
            exit 2
    esac
done
shift `expr $OPTIND - 1`
OPTIND=1


SRCDIR="/rsrch3/home/thera_dis/p_eclipse/workspace/inbox/sequencers:/rsrch1/thera_dis/Eclipse"
TGTDIR=/rsrch3/home/thera_dis/p_eclipse_combio/workspace/runs

for i in $*; do
    run=$(basename $i)
    mkdir -p $TGTDIR/$run

    for d in $(echo $SRCDIR | sed -e 's/:/ /g'); do
        if [ -d $d/$run ]; then
            if [ $MODE == "copy" ]; then
                mkdir -p $TGTDIR/$run/bcl
                rsync -az $SRCDIR/${run}/ $TGTDIR/$run/bcl/
            else
                ln -snf $d/$run $TGTDIR/$run/bcl
            fi
            break
        fi
    done
done
