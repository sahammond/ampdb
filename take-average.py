#!/usr/bin/env python2

import sys 

import pandas as pd
import argparse


def loader(data, header, rows):
    print 'Reading ' + data
    dat = pd.read_csv(data, header=None, sep=' ', names=header)
    dat['row'] = rows
    dat.set_index('row', inplace=True)
    return dat


def main():
    parser = argparse.ArgumentParser(description='calculate average absorbance per well')
    parser.add_argument('plate', action='store', nargs='+', help='plain text mic plate reader data')
    parser.add_argument('--name', '-n', required=True, action='store',
                        help='name of the assay as in db')
    args = parser.parse_args()
    plates= args.plate
    
    header = range(1, 13)
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    r1 = loader(plates[0], header, rows)
    r2 = loader(plates[1], header, rows)
    r3 = loader(plates[2], header, rows)
    
    if len(r1.columns) != 12 or len(r2.columns) != 12 or len(r3.columns) != 12:
        print 'One or more of the input files does not have the expected 12 columns of data.'
        print 'Check for missing decimals or other problems.'
        sys.exit(1)
    
    frames = [r1, r2, r3]
    dat = pd.concat(frames)
    
    res = dat.groupby('row').mean()
    if len(res.columns) != 12:
        print 'The average data does not have 12 columns; there is likely a problem with the input.'
        print 'Check input for non-numerical characters.'
        sys.exit(1)
    outname = ''.join([args.name, '-average.txt'])
    print 'Writing ' + outname
    res.to_csv(outname, sep=' ', index=False, header=False, float_format='%.3f')


if __name__ == '__main__':
    main()
