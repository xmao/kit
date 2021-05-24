#!/usr/bin/env sh

awk -F "\t" '{ printf("%s\t%i\t%i\n", $1, $2-1, $3); }'
