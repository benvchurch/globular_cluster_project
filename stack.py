import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from astropy.utils.data import download_file
from astropy.io import fits
from astropy.stats import sigma_clipped_stats



def stack_images(image_file_base, outfile):
	image_list = [ fits.open(image_file_base + str(n) + ".fits") if n > 9 else fits.open(image_file_base + '0' + str(n) + ".fits") \
              for n in range(1,14) ]

	print(image_list[0], image_list[0][0], image_list[0][0].header)

	image_concat = [ image[0].data for image in image_list ]

	final_image = np.sum(image_concat, axis=0)

	# take background statistics of the image
	mean, median, std = sigma_clipped_stats(final_image, sigma=10.0)

	subt_data = np.vectorize(lambda x: x if x >= 0 else 0)(final_image - median)
	maximum = np.quantile(subt_data.flatten(), 0.99)

	#plot histagram

	#image_hist = plt.hist(subt_data.flatten(), 1000)
	#plt.show()

	# show the image
	# plt.imshow(subt_data, cmap='gray', vmin = 0, vmax = maximum)
	# plt.colorbar()
	# plt.show()

	out_image = image_list[0]
	out_image[0].data = subt_data

	fits.writeto(outfile, out_image[0].data, out_image[0].header, overwrite=True)


# image_file_base = "20_13_27/M3_000"
# outfile = 'M3_processed.fits'

# stack_images(image_file_base, outfile)
