#!/usr/bin/env Rscript

# get-matrix-count count/Sample1
args <- commandArgs(T)
D <- Seurat::Read10X(file.path(args[1], "outs", "filtered_feature_bc_matrix"))

D.all <- data.frame(gene = rownames(D), totalUMIs = Matrix::rowSums(D))

odir <- ifelse (length(args) == 1, dirname(args[1]), args[2])
write.csv(D.all, file.path(odir, sprintf("%s-TotalUMIs.csv", basename(args[1]))), quote = F)
