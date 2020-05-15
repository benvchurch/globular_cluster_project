import numpy as np

from astropy.io import fits
from astropy.stats import gaussian_sigma_to_fwhm
from astropy.stats import sigma_clipped_stats
from photutils.utils import cutout_footprint

from photutils.background import MADStdBackgroundRMS
from photutils.psf import IntegratedGaussianPRF
from photutils.psf import DAOPhotPSFPhotometry
from photutils import DAOStarFinder
from photutils import CircularAperture



def find_stars(data):

	# take background statistics of the image
	mean, median, sig = sigma_clipped_stats(data, sigma=10.0)

	bkgrms = MADStdBackgroundRMS()
	std = bkgrms(data)

	# setup calibration parameters

	thresh = 5. * std # detect stars at 5-sigma level
	sigma_psf = 5. # size in pixels of targets
	fwhm_sigma = sigma_psf * gaussian_sigma_to_fwhm # convert to full-width at half-maximum

	subt_data = data - median
	maximum = np.quantile(subt_data.flatten(), 0.99)

	# DAOStarFinder

	stfind = DAOStarFinder(threshold=thresh, fwhm=fwhm_sigma)
	sources = stfind(subt_data)
	positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
	return positions
