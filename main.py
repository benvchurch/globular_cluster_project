

# for each cluster first for each filter (if no processed file exists) make stacked file

# then load all five filter images

# stack them and use this to find stars

# for each filter image run take photometry for each star

# compute parameters of the cluster

# make plots

import os.path
from os import path
from stack import stack_images
from find_stars import *
from photometry import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from analysis import *

cluster_list = ['M3', 'M5']
filter_list = ['F4','F5']
base_directory = "../cluster_data/"
plot_directory = "../plots/"

def path_name(clust, F):
	return base_directory + clust + '/' + F + '/' + clust + F +  "_processed.fits"

clust_resutls = []

for clust in cluster_list:
	for F in filter_list:
		if not path.exists(path_name(clust, F)):
			stack_images(base_directory + clust + '/' + F + '/' + clust + '_000', path_name(clust, F))

	image_list = [ fits.open(path_name(clust, F))  for F in filter_list ]

	data_list = [ image[0].data for image in image_list ]
	all_band_image = np.sum(data_list, axis=0)

	# print out the processed images

	for (F, data) in zip(filter_list, data_list):
		maximum = np.quantile(data.flatten(), 0.99)
		fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(12,16))
		plt.title(clust)
		plt.imshow(data, cmap='gray', vmin = 0, vmax = maximum)
		plt.colorbar()
		fig.savefig(plot_directory + clust + F + 'processed.pdf', dpi=300, bbox_inches='tight')
		plt.close(fig)


	# find star positions
	positions = find_stars(all_band_image)

	# make a plot of the idenified stars
	fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(12,16))
	plt.title('DAOStarFinder')
	maximum = np.quantile(all_band_image.flatten(), 0.99)
	plt.imshow(all_band_image, cmap='gray', interpolation='nearest', vmin = 0, vmax = maximum)
	apertures = CircularAperture(positions, r=4.)
	apertures.plot(color='red', lw=1.5)

	fig.savefig(plot_directory + clust + F + 'identified.pdf', dpi=300, bbox_inches='tight')
	plt.close(fig)
	# do photometry on the bands
	star_list = calculate_photometry(data_list, positions)

	# make HR diagram
	make_hr_diagram(star_list, clust, plot_directory)
	# make_m_diagram(star_list, clust, plot_directory)

	clust_resutls.append([clust, fit_cluster_shape(positions), avg_color(star_list), avg_metal(star_list)])

print clust_resutls
