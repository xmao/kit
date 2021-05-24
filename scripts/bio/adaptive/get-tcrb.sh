#!/usr/bin/env sh

xsv select amino_acid,templates,productive_frequency $1 | sed -e 1d
