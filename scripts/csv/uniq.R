#!/usr/bin/env Rscript

args <- commandArgs(T)

D <- read.delim(args[1], as.is=T, check.names=F)

DD <- D[!duplicated(D[[2]]), ]

write.table(DD, sep='\t', quote=F, row.names=F)
