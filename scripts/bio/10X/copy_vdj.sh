#!/usr/bin/env sh

set -e

TARGET="result"

while getopts :t: OPT; do
    case $OPT in
        t|+t)
            TARGET="$OPTARG"
            ;;
        *)
            echo "usage: `basename $0` [+-t ARG} [--] ARGS..."
            exit 2
    esac
done
shift `expr $OPTIND - 1`
OPTIND=1

SOURCE="${1:-.}"

for TYPE in count vdj; do
    if [ -d $SOURCE/$TYPE ]; then
        mkdir -p $TARGET/$TYPE
        for i in `find $SOURCE/$TYPE  -mindepth 1 -maxdepth 1 -type d`; do
            echo "Copying $i ..."
            mkdir $TARGET/$TYPE/$(basename $i)
            rsync -az $i/outs/ $TARGET/$TYPE/$(basename $i)/
        done
    fi
done

