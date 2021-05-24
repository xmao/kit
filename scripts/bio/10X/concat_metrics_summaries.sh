#!/usr/bin/env bash

files=( ${@:-*/outs/metrics_summary.csv} )

paste -d ',' \
      <(echo "Sample ${files[@]}" | tr ' ' '\n') \
      <(csvtk concat ${files[@]}) | \
    sed -e '2,$s/\/outs\/metrics_summary.csv//' | tee metrics_summaries.csv
