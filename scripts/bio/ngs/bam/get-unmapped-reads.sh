#!/usr/bin/env bash

set -ex

samtools view -@ 8 -u -f 4 -F 264 $1 -o ${1%.bam}.R1.only.unmapped.bam
samtools view -@ 8 -u -f 8 -F 260 $1 -o ${1%.bam}.R2.only.unmapped.bam
samtools view -@ 8 -u -f 12 -F 256 $1 -o ${1%.bam}.R1R2.both.unmapped.bam

samtools merge -@ 8 -u - \
         ${1%.bam}.R1.only.unmapped.bam ${1%.bam}.R2.only.unmapped.bam ${1%.bam}.R1R2.both.unmapped.bam \
    | samtools sort -O bam -@ 8 -n -o ${2:-${1%.bam}.R1R2.any.unmapped.bam} -
