#!/usr/bin/env sh

awk 'BEGIN{ total=0; } { total += $3 - $2 + 1; } END{ print total; }'
