#!/usr/bin/bash

binName=`echo $1 | cut -d '.' -f 1`
gcc ./$1 -o $binName.bin -s
