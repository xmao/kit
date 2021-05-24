#!/usr/bin/env bash

# set -x
read -p "User: " -r USER
read -p "Password: " -r -s PASSWORD
echo

for f in $*; do
    echo -n -e "Uploading $f ... "
    curl -s -k --ftp-ssl --ftp-pasv --ftp-create-dirs \
         -u "$USER:$PASSWORD" \
         -T $f ftp://ftps.mdanderson.org/$(dirname $f)/
    if [ $? -eq 0 ]; then echo "Done"; else echo "Failed"; echo $f >> failed-files.txt; fi
done
