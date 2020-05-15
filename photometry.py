from photutils import aperture_photometry, CircularAperture
from star_data import *

def calculate_photometry(image_list, positions):
    num_filters = len(image_list)
    apertures = CircularAperture(positions, r=5.)
    band_data = [aperture_photometry(data, apertures)['aperture_sum'] for data in image_list]

    print band_data[0][0], band_data[1][0], len(positions), num_filters

    star_list = []
    for i in range(0, len(positions)):
        s = star_data(positions[i], [band_data[j][i] for j in range(0, num_filters)])
        star_list.append(s)

    return star_list
