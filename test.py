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
data = hdulist[0].data
hdulist.close()


# Crop image
# crop = cutout_footprint(hdu_data, (1200, 600), (600, 1200))
# hdu_crop = crop[0]

# take background statistics of the image
mean, median, sig = sigma_clipped_stats(data, sigma=10.0)

bkgrms = MADStdBackgroundRMS()
std = bkgrms(data)

# setup calibration parameters

print(mean, median, std)

thresh = 5. * std # detect stars at 5-sigma level
sigma_psf = 5. # size in pixels of targets
fwhm_sigma = sigma_psf * gaussian_sigma_to_fwhm # convert to full-width at half-maximum

subt_data = data - median
maximum = np.quantile(subt_data.flatten(), 0.99)

print median



# DAOStarFinder

stfind = DAOStarFinder(threshold=thresh, fwhm=fwhm_sigma)
sources = stfind(subt_data)
print(sources[0])

# photometry

from photutils import aperture_photometry, CircularAperture
positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
apertures = CircularAperture(positions, r=5.)

phot_table = aperture_photometry(subt_data, apertures)
for col in phot_table.colnames:
    phot_table[col].info.format = '%.8g'  # for consistent table output
print(phot_table)


# median, std = np.median(hdu_crop), np.std(hdu_crop)

plt.title('DAOStarFinder')
# plt.imshow(subt_data, cmap='viridis', aspect=1, interpolation='nearest',
#           origin='lower', vmin=0., vmax=median + std)

plt.imshow(subt_data, cmap='gray', interpolation='nearest', vmin = 0, vmax = maximum)
plt.colorbar()

positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
apertures = CircularAperture(positions, r=4.)
apertures.plot(color='red', lw=1.5)
plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)


plt.show()

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

print clf.means_, clf.covariances_

CS = plt.contour(X, Y, Z, norm=LogNorm(vmin=1.0, vmax=1000.0),
                 levels=np.logspace(np.log(16), np.log(20), 10))

plt.scatter(X_train[:, 0], X_train[:, 1], .8)

plt.title('Negative log-likelihood predicted by a GMM')
plt.axis('tight')
plt.show()
