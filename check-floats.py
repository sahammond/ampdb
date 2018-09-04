#!/usr/bin/env python2

import sys

table = sys.argv[1]

with open(table, 'r') as infile:
    for line in infile:
        rec = line.strip().split(' ')
        for val in rec:
            try:
                float(val)
            except ValueError:
                print '%s is not a float' % val
