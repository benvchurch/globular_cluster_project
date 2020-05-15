# filters apertures
# 0 - h-alpha
# 1 - clear
# 2 - B
# 3 - V
# 4 - R

import numpy as np

class star_data:
    '''Class for keeping track of a Star'''
    pos = None
    luminosity_bands = None
    total_luminosity = None

    def tot_mag(self):
        return -2.5*np.log10(self.total_luminosity)

    def band_mag(self, i):
        return -2.5*np.log10(self.luminosity_bands[i])

    def BV_col(self):
        return self.band_mag(2) - self.band_mag(3)
        # CHANGE THIS TO 2 and 3

    def VR_col(self):
        return self.band_mag(3) - self.band_mag(4)

    # metalicity sensitive metal abundance index (e.g. Hilker) should be Y not R but you work with what you got

    def m1(self):
        return self.band_mag(3) - 2 * self.band_mag(2) + self.band_mag(4)

    def __init__(self, pos, bands):
        self.pos = pos
        self.luminosity_bands = bands
        self.total_luminosity = bands[1] # the second filter is clear
