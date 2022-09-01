import torch
import time
from pdb import set_trace
import os
import numpy as np
import openslide
import extract_tissue
import shutil
import math
import glob
import argparse

parser = argparse.ArgumentParser(description="Params")
parser.add_argument( "--source", nargs="?", type=str, help='path to folder containing raw wsi image files')
parser.add_argument( "--out_path", nargs="?", type=str, default='test_coords.csv', help='a file listing all patch coordinates')
parser.add_argument( "--otsu", nargs="?", type=bool, default=True)
parser.add_argument( "--zoom", nargs="?", type=int, default=20)

if __name__ == '__main__':

    args = parser.parse_args()

    source = args.source
    with open(source, 'r') as f:
        slides = f.read().splitlines()
    #slides = sorted(os.listdir(source))
    #slides = [slide for slide in slides if os.path.isfile(os.path.join(source, slide))]
    #slides_to_read = ["testing_images/1.svs","testing_images/2.svs","testing_images/3.svs"] # list of testing whole slide images

    coord_file_path = args.out_path
    coord_file = open(coord_file_path, 'w')  # a file listing all patch coordinates

    do_otsu = args.otsu
    zoom = args.zoom

    if do_otsu:
        ### get coordinates of tissue patches in whole slide images using Otsu algorithm ###
        for image_path in slides:
            slide = openslide.OpenSlide(os.path.join(image_path))
            slide_id = os.path.splitext(os.path.basename(image_path))[0]
            grid, _ = extract_tissue.make_sample_grid(slide, 256,
                                                      zoom, 10, 10, False, prune=False, overlap=0)
            for (x,y) in grid:
                coord_file.write('{},{},{},0\n'.format(slide_id, x, y))
    else:
        ### get coordinates of all patches in whole slide images ###
        stride = 256
        for image_path in slides:
            slide = openslide.OpenSlide(os.path.join(image_path))
            slide_id = os.path.splitext(os.path.basename(image_path))[0]
            slide_zoom = int(slide.properties[openslide.PROPERTY_NAME_OBJECTIVE_POWER])
            ds_factor = slide_zoom/zoom
            best_ds_level = slide.get_best_level_for_downsample(ds_factor)
            image_size = slide.level_dimensions[best_ds_level]
            for ii in range(0,image_size[0],stride):
                for jj in range(0,image_size[1],stride):
                    coord_file.write('{},{},{},0\n'.format(slide_id, ii, jj))