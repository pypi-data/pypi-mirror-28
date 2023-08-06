#!/bin/bash

echo '##########################################'
echo '###   Compile the C shared libraries   ###'
echo '##########################################'
echo

# Detect the platform
case $OSTYPE in
    darwin*) platform=osx;;
    linux*) platform=linux;;
esac
echo "Detected platform: $platform"
echo

# Variables
dir=sources
prefix=Integrand

# Char lengths
dirchrlen=${#dir}
prechrlen=${#prefix}

# Compile
for entry in "$dir"/*
do
    chrlen=${#entry}
    fullname="${entry:dirchrlen+1:chrlen-dirchrlen-1-2}"
    startwith="${entry:dirchrlen+1:prechrlen}"

    if [ $startwith = "Integrand" ] && [[ ${#fullname} -gt 19 ]]; then
        srcname="$dir/$fullname.c"
        outname="$platform/$fullname.so"
    	echo "Compile $srcname"
        gcc -shared -o $outname -fPIC -lm -lgsl $srcname
    fi
done

echo
echo "The job is done."
echo

exit 0
