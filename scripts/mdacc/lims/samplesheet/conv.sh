#!/usr/bin/env bash

set -e

in2csv -I $1 1>${1%.xlsx}.csv 1> >(tee ${1%.xlsx}.csv) 2> >(grep -v -i warning 1>&2)
