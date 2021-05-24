#!/usr/bin/env sh

METHOD='signed_pvalue'

while getopts ":m:" OPT; do
    case "$OPT" in
        m|+m)
            METHOD=$OPTARG
            ;;
        *)
            echo "$OPT Didn't match anything"
    esac
done
shift $(($OPTIND - 1)); OPTIND=1

if [ $METHOD == "signed_pvalue" ]; then
    cat ${1:-} \
        | xsv select gene_symbol,logFC,PValue | xsv fmt -t "\t" \
        | awk 'FNR > 1 { s = ($2 >= 0) ? -1 : 1; printf("%s\t%f\n", $1, s * log($3) / log(10)); }' \
        | tr 'a-z' 'A-Z'
elif [ $METHOD == "unsigned_pvalue" ]; then
     cat ${1:-} \
        | xsv select gene_symbol,logFC,PValue | xsv fmt -t "\t" \
        | awk 'FNR > 1 { printf("%s\t%f\n", $1, -log($3) / log(10)); }' \
        | tr 'a-z' 'A-Z'
 else
     cat ${1:-} \
        | xsv select gene_symbol,logFC | xsv fmt -t "\t" | sed -e 1d | tr 'a-z' 'A-Z'
fi


