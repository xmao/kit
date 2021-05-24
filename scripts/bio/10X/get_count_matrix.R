#!/usr/bin/env Rscript
# get-matrix-count count/Sample1

args <- commandArgs(T)

D <- Seurat::Read10X(file.path(args[1], "outs", "filtered_feature_bc_matrix"))

odir <- ifelse (length(args) == 1, dirname(args[1]), args[2])

write.csv(D, file.path(odir, sprintf("%s.csv", basename(args[1]))), quote = F)
