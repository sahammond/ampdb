#!/bin/bash

prefix=$1

x=1
while read line; do
    /projects/amp/in_vitro/results/scripts/take-average.py --name=${prefix}-plate-$x $line
    ((x+=1))
done < replicate-reads.txt
