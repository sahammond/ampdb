#!/bin/bash

# adds 0 values for the empty rows in the plates for layout 2

awk '{
    a=$0;
    getline;
    b=$0;
    getline;
    c=$0;
    getline;
    d=$0;
    getline;
    e=$0;
    getline;
    print a"\n"b"\n"0"\n"c"\n"d"\n"0"\n"e"\n"$0
    }' $1
