from dataclasses import dataclass

@dataclass
class star_Data:
    '''Class for keeping track of a Star'''
    pos: (float, float)
    luminosity_band: list
    total_luminosity: float

    def tot_mag(self):
	return -2.5*np.log10(total_luminosity)

    def BV_mag(self):
        #DO THIS

    def UV_mag(self):
        #DO THIS
