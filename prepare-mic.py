#!/usr/bin/env python

import sys
import re
import argparse


def builder(plates, start, name, assay, isolate, layout, exp_date, mic):
    """build insert statement lines"""
    plateno = 1
    rid = start # record ID
    readno = 1
    segno = 1
    for plate in plates:
        seg = plateno * 8
        startseg = seg - 8
        segment = layout[startseg:seg]
        plate_mic = mic[startseg:seg]
        with open(plate, 'r') as infile:
            # 3 reads per plate
            front = 'INSERT INTO `mic` VALUES ('
            sep = ','
            row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            row_num = 0
            for line in infile:
                this_row = row[row_num]
                pep = segment[row_num].split(' ')[0]
                this_mic = plate_mic[row_num]
                # note that blood is hard-coded to NA right now
                buff = [str(rid), str(assay), str(isolate), '1', str(pep), name, 'assayed', 'experiment',
                        str(readno), exp_date, this_row]
                rec = line.strip().split(' ')
                buff.extend(rec)
                buff.extend([this_mic, 'NA'])
                buff_form = buff[:5] + ["'" + x + "'" for x in buff[5:]] + ['NULL', 'NULL);']
                outbuff = front + ','.join(buff_form)
                outbuff = re.sub("experiment','4',","experiment','AVERAGE',",outbuff)

                # increment counters
                rid += 1
                if row_num == 7:
                    row_num = 0
                    if readno == 4: # assumes 3 reads and an average
                        plateno += 1
                        readno = 1
                    else:
                        readno += 1
                else:
                    row_num += 1

                yield outbuff


def load_layout(layout_file):
    lay = []
    with open(layout_file, 'r') as infile:
        for line in infile:
            lay.append(line.strip())

    return lay


def load_mic(mic_file):
    mic = []
    with open(mic_file, 'r') as infile:
        for line in infile:
            mic.append(line.strip())

    return mic


def main():
    parser = argparse.ArgumentParser(description='add plates of mic data to the mysql db')
    parser.add_argument('plate', action='store', nargs='+', help='plain text mic plate reader data')
    parser.add_argument('--name', '-n', required=True, action='store',
                        help='name of the assay as in db')
    parser.add_argument('--start', '-s', required=True, action='store', type=int,
                        help='id to begin inserting into table at')
    parser.add_argument('--isolate', '-i', required=True, action='store', type=str,
                        help='numeric id of the isolate used')
    parser.add_argument('--assay', '-a', required=True, action='store', type=str,
                        help='numeric id of the assay in db')
    parser.add_argument('--date', '-d', required=True, action='store', type=str,
                        help='date experiment performed, as 2018-08-02 00:00:00')
    parser.add_argument('--layout', '-l', required=True, action='store', type=str,
                        help='single column peptide names with blanks if applicable')
    parser.add_argument('--mic', '-m', required=True, action='store', type=str,
                        help='single column mic values with blanks and mic > 256 as 0')
    args = parser.parse_args()

    layout = load_layout(args.layout)
    mic = load_mic(args.mic)
    for line in builder(args.plate, args.start, args.name, args.assay, args.isolate,
                        layout, args.date, mic):
        print line


if __name__ == '__main__':
    main()
