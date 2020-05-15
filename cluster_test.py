import matplotlib.pyplot as plt
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

# Load data.
image_file = 'M3_processed.fits'

# Image data.
hdulist = fits.open(image_file)
print(hdulist[0].header)
xsize = hdulist[0].header['NAXIS1']
ysize = hdulist[0].header['NAXIS2']
hdu_data = hdulist[0].data
hdulist.close()

# Crop image

hdu_crop = hdu_data

# take background statistics of the image
mean, median, std = sigma_clipped_stats(hdu_data, sigma=10.0)  

# setup calibration parameters

print(mean, median, std)

thresh = 5. * std # detect stars at 5-sigma level
sigma_psf = 5. # width in pixels of targets
fwhm_sigma = sigma_psf * gaussian_sigma_to_fwhm # convert to full-width at half-maximum
fitshape = int(3 * np.ceil(fwhm_sigma) // 2 * 2 + 1)

subt_data = hdu_crop - median
maximum = np.quantile(subt_data.flatten(), 0.99)

print median


# DAOStarFinder

stfind = DAOStarFinder(threshold=thresh, fwhm=fwhm_sigma)
sources = stfind(subt_data)  
print(type(sources))


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from sklearn import mixture

X_train = np.array(zip(sources['xcentroid'], sources['ycentroid']))

from matplotlib.colors import LogNorm
from sklearn import mixture


clf = mixture.GaussianMixture(n_components=1, covariance_type='full')
clf.fit(X_train)


# display predicted scores by the model as a contour plot

x = np.linspace(0, xsize)
y = np.linspace(0, ysize)
X, Y = np.meshgrid(x, y)
XX = np.array([X.ravel(), Y.ravel()]).T
Z = -clf.score_samples(XX)
Z = Z.reshape(X.shape)

centroid = clf.means_[0]
covariance = clf.covariances_[0]

evals = np.linalg.eig(covariance)[0]
Casp = np.sqrt(abs(evals[0] - evals[1])/(evals[0] + evals[1]))

print Casp

CS = plt.contour(X, Y, Z, norm=LogNorm(vmin=1.0, vmax=25.0),
                 levels=np.logspace(np.log10(10), np.log10(20), 10))

plt.scatter(X_train[:, 0], X_train[:, 1], .8)

plt.title('Negative log-likelihood predicted by a GMM')
plt.axis('tight')
plt.show()

def radius(pos, center):
	return np.sqrt((pos[0] - center[0])**2 + (pos[1] - center[1])**2) 

radii = [radius(star_pos, centroid) for star_pos in X_train]

plt.hist(radii, 50)
plt.show()


