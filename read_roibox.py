
import numpy as np
import argparse
import os

import scipy.io

from bs4 import BeautifulSoup
import openslide
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

'''
The aim of this piece of script is to extract the coordinates of rectangular regions of interest (boxes) obtained from 
Hamamatsu viewer (NDP.view) and to visualize them onto a segmentation file obtained from our modified version of 
DMMN framework.

Input:
Box.ndpa = the box obtained from saving 
'''

parser = argparse.ArgumentParser(description="Params")
parser.add_argument( "--source_file", nargs="?", type=str, help='text file containing the paths to ndpi and Box files)')
parser.add_argument( "--seg_file", nargs="?", type=str, help='path to file containing paths to the segmentation files')
parser.add_argument( "--out_path", nargs="?", type=str, default='.', help=' folder where to store all the new figures')
parser.add_argument( "--ds", nargs="?", type=int, default=64, help='Down sampling factor')

if __name__ == '__main__':

	args = parser.parse_args()

	source_file = args.source_file
	with open(source_file, 'r') as f_source:
		path2slides = f_source.read().splitlines()

	seg_file = args.seg_file
	with open(seg_file, 'r') as f_seg:
		path2segs = f_seg.read().splitlines()

	# loop over all the entries
	for slide_path, seg_path in zip(path2slides, path2segs):

		#
		slide = openslide.OpenSlide(slide_path)
		box = slide_path + '.ndpa'
		seg = scipy.io.loadmat(seg_path)
		seg = seg['seg']
		#
		slide_id = os.path.splitext(os.path.basename(slide_path))[0]

		#  down sampling level
		ds = args.ds
		# Set the best level for the selected down sampling level
		best_level = slide.get_best_level_for_downsample(ds)


		# Reading the data inside the xml file to a variable under the name  data
		with open(box, 'r') as f:
			data = f.read()

		# Passing the stored data inside the beautifulsoup parser
		bs_data = BeautifulSoup(data, 'xml')


		# Finding all instances of tag
		b_unique = bs_data.find_all('ndpviewstate')
		print(b_unique)

		# Kow many ROI BOC are there?
		n_box = len(b_unique)
		box_info = []

		# get slide dimension (pixel)
		xSize = slide.dimensions[0]
		ySize = slide.dimensions[1]

		# get voxel real dimension (convert from um to nm)
		pix2nm_x = float( slide.properties[openslide.PROPERTY_NAME_MPP_X] )*1e3
		pix2nm_y = float( slide.properties[openslide.PROPERTY_NAME_MPP_Y] )*1e3

		# Get X and Y offset (this represents the position of the centre from the offset point in nm)
		xOffset = float( slide.properties['hamamatsu.XOffsetFromSlideCentre'] )
		yOffset = float( slide.properties['hamamatsu.YOffsetFromSlideCentre'] )

		# Plot
		fig_overlay = plt.figure()
		fig_overlay1 = np.array(
			slide.read_region((0, 0), best_level, slide.level_dimensions[best_level]).convert('L')) / 255.0
		overlay2 = seg
		plt.imshow(fig_overlay1, cmap='gray')
		plt.imshow(overlay2, cmap='Dark2', alpha=0.5)
		plt.clim(0, 7)
		plt.colorbar()
		plt.xticks([])
		plt.yticks([])
		# plt.show()

		# loop over all the ndpviewstate (i.e. the boxes)
		for child in b_unique:

			# parse the field corresponding to the points
			print(child)
			points = child.find_all('point')

			# following coordinates are in Sys Of Ref centered in the offSet point (expressed in nm)!!!

			# x0 and y0 are the top-left corner coordinates
			x0 = float( points[0].x.contents[0])
			y0 = float( points[0].y.contents[0])
			# y1 is the bottom points y coordinate
			y1 = float( points[1].y.contents[0])
			# x3 is the rightmost points x coordinate
			x3 = float( points[3].x.contents[0])

			# Following coordinates represent the offset point in the SOR centered in the top left corner of the slide
			# (in pixels)
			Ox = int(xSize / 2) - int(xOffset / pix2nm_x)
			Oy = int(ySize / 2) - int(yOffset / pix2nm_y)

			# This is the location of the top left corner of the box wrt SOR centered in left-top corner (in pixels).
			location = (int(x0/pix2nm_x) + Ox, int(y0/pix2nm_y) + Oy )
			# Width anf height of the box in pixels
			size = ( int( (x3 - x0)/pix2nm_x ), int( (y1 - y0)/pix2nm_y))


			currentAxis = plt.gca()
			currentAxis.add_patch(
				Rectangle( (location[0]/ds, location[1]/ds), int(size[0]/ds), int(size[1]/ds) ,
											 facecolor="none", ec='r', lw=1))

		fig_overlay.savefig(os.path.join(args.out_path, slide_id) + '_overlay.png', dpi=800)
		plt.close()