#!/usr/bin/env Rscript

options(error = function() {
    cat("\nTraceback:\n"); traceback(2)
    if(!interactive()) quit("no", status = 1, runLast = FALSE)
})


if (interactive() == FALSE) {
    suppressPackageStartupMessages(library(argparse))
    library(plyr)

    parser <- ArgumentParser(description="Calculate common regions with low coverage across multiple samples")
    parser$add_argument('files', type='character', nargs=1, help='List of files including per-target coverage analysis from Picard by default')
    parser$add_argument('-c', '--cutoff', type='double', default=0.2, help='Cutoff of percentage of low coveage against average total coverage')
    parser$add_argument('-S', '--statistics', type='character', nargs=1, help='List of corresponding files of coverage statistics all targets')

    if (length(commandArgs(T)) == 0) {
        stop(parser$print_help())
    } else {
        args <- parser$parse_args()   
    }

    args$files <- readLines(args$files)
    args$statistics <- paste(readLines(args$statistics), collapse=',')
    q
    D <- lapply(args$files, function(f) {
        read.delim(f, as.is=T, stringsAsFactors=F)
    })

    A <- sapply(strsplit(args$statistics, ',')[[1]], function(f) {
        read.delim(f, comment.char='#', as.is=T, stringsAsFactors=F)[['MEAN_TARGET_COVERAGE']]
    })

    DD <- do.call(cbind.data.frame, lapply(D, function(x) x[7]))
    colnames(DD) <- sub('.*T3001-', '', sub('_.*', '', basename(args$files)))

    DDD <- t(apply(DD, 1, function(x) x/A))

    DDDD <- cbind.data.frame(D[[1]][1:6], status=apply(DDD, 1, function(x) all(x<0.2)), DD)

    ## print(DDDD[1:50, ])
    write.table(DDDD[DDDD[['status']] == T, ], sep='\t', quote=F, row.names=F)
}
