# filters apertures
# 0 - h-alpha
# 1 - clear
# 2 - B
# 3 - G
# 4 - R

import numpy as np

# parameters to transform from BGR to BVR from https://arxiv.org/pdf/1501.04778.pdf

C1 = np.array([-0.291,-0.252,-0.226])
C2 = np.array([0.280,0.542,0.051])
C3 = np.array([0.600,-0.471,0.468])

def transform_BGR_to_BVR(data):
	return C1 + data +  np.array([m * (data[0] - data[1]) for m in C2]) +  np.array([m * (data[1] - data[2]) for m in C3])

class star_data:
    '''Class for keeping track of a Star'''
    pos = None
    luminosity_bands = None
    total_luminosity = None
    mag_BGR = None
    mag_BVR = None

    def tot_mag(self):
		if self.total_luminosity == 0:
			print 'Zero Lumen ' + str(self.pos)
			return 0
		return -2.5*np.log10(self.total_luminosity)

    def band_mag(self, i):
		if self.luminosity_bands[i] == 0:
			print 'Zero Lumen ' + str(self.pos)
			return 0
		return -2.5*np.log10(self.luminosity_bands[i])

    def BR_col(self):
        return self.mag_BGR[0] - self.mag_BGR[2]
        
    def BG_col(self):
        return self.mag_BGR[0] - self.mag_BGR[1]    

    def BV_col(self):
        return self.mag_BVR[0] - self.mag_BVR[1]

    def VR_col(self):
        return self.mag_BVR[1] - self.mag_BVR[2]

    # metalicity sensitive metal abundance index (e.g. Hilker) should be Y not R but you work with what you got

    def m1(self):
        return self.mag_BVR[1] - 2*self.mag_BVR[0] + self.mag_BVR[2]

    def __init__(self, pos, bands):
		self.pos = pos
		self.luminosity_bands = bands
		self.total_luminosity = bands[1] # the second filter is clear
		self.mag_BGR =  np.array([self.band_mag(i) for i in range(2,5)])
		self.mag_BVR = transform_BGR_to_BVR(self.mag_BGR)
		
