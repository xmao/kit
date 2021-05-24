#!/usr/bin/env sh

samtools idxstats $1 | cut -f1 | grep -v -e '*' -e '^\(GL\)\|\(NC\)\|\(MT\)'
