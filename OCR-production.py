#!/usr/bin/env python3

import glob
import os
import io
import re
import sys

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image
from IPython import display

from google.cloud import storage
from google.cloud import vision
from google.protobuf import json_format

img_files = sys.argv[1:]


def gen_rect_coords(verts):
    x = verts[0].x
    y = verts[1].y
    width = verts[2].x - x
    height = verts[2].y - y
    return (x, y), width, height


def plot_bounding_box(img_file, predicted_texts):
    fig, ax = plt.subplots(1, figsize=(16, 14))

    im = np.array(Image.open(img_file), dtype=np.uint8)
    ax.imshow(im, cmap='Greys')


    for k, text in enumerate(predicted_texts):
        if k == 0:
            continue # skip the global bounding box
        (x, y), width, height = gen_rect_coords(text.bounding_poly.vertices)
        rect = patches.Rectangle((x, y), width, height, linewidth=0.8, edgecolor='yellow', facecolor='none')
        ax.add_patch(rect)

    plt.axis('off')
    out = img_file.replace('.invert_color.png', '.bounding-box.png')
    plt.savefig(out, dpi=300, bbox_inches='tight')
    fig.clf()
    plt.close()


"""Detects document features in an image."""
client = vision.ImageAnnotatorClient()

for k, img_file in enumerate(img_files):
    with io.open(img_file, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    #get_ipython().run_line_magic('time', 'response = client.text_detection(image=image)')
    response = client.text_detection(image=image)
    predicted_texts = response.text_annotations

    plot_bounding_box(img_file, predicted_texts)
    
    out_txt = img_file.replace('.invert_color.png', '.txt')
    print(f'writing {out_txt} ...')
    with open(out_txt, 'wt') as opf:
        opf.write(predicted_texts[0].description)
