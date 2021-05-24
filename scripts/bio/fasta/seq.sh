#!/usr/bin/env sh

for i in $*; do
    sed -n -e '2~2p' $i | awk '{ print length; }'
done
