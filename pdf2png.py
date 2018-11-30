#!/usr/bin/env python3
"""convert and split pdf of plate scans to png files"""
# Written by Zhuyi Xue, BCGSC
# Modified by S. Austin Hammond, BCGSC

import os
import sys
from IPython.display import Image

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wand.image import Image as WImage
from PyPDF2 import PdfFileWriter, PdfFileReader


input_pdf_file = sys.argv[1]

def write_page_pdf(page_pdf, outfile):
    print(f'writing {outfile} ...')
    output = PdfFileWriter()
    output.addPage(page_pdf)
    with open (outfile, "wb") as opf:
        output.write(opf)


def to_jpg(page_pdf, outfile, box):
    img = WImage(filename=page_pdf, resolution=300)
    img.rotate(-0.4)
    width, height = img.size
    if box == 'bottom':
        img.crop(left=int(width * 0.1), top=int(height * 0.660), right=int(width * 0.93), bottom=int(height * 0.79))
    elif box == 'top':
        img.crop(left=int(width * 0.1), top=int(height * 0.2425), right=int(width * 0.93), bottom=int(height * 0.366))
    img.type = 'grayscale'
    print(f'writing {out_page_jpg} ...')
    img.save(filename=out_page_jpg)


def invert_grey(infile, outfile):
    """It seems helpful by turning background black"""
    im = np.array(Image.open(infile), dtype=np.uint8)
    fig, ax = plt.subplots(1, figsize=(16, 14))
    ax.imshow(im, cmap='Greys')
    plt.axis('off')
    print(f'writing {outfile} ...')
#     plt.savefig(outfile, dpi=300, bbox_inches='tight')
    # Performance deteriorates with bbox_inches='tight' 
    plt.savefig(outfile, dpi=300)
    fig.clf()
    plt.close()

bname = os.path.basename(input_pdf_file)
outdir = os.path.dirname(input_pdf_file)

with open(input_pdf_file, "rb") as inf:
    input_pdf = PdfFileReader(inf)

    for page in range(input_pdf.getNumPages()):
        out_page_pdf = os.path.join(outdir, f'page{page}.pdf')
        write_page_pdf(input_pdf.getPage(page), out_page_pdf)
        for box in ('top', 'bottom'):
            # this seems to have to be jpg, other wise inverting color becomes strange
            out_page_jpg = os.path.join(outdir, f'page{page}.{box}.cropped.jpg')
            to_jpg(out_page_pdf, out_page_jpg, box)

            out_page_png = os.path.join(outdir, f'page{page}.{box}.invert_color.png')
            invert_grey(out_page_jpg, out_page_png)
