from dataclasses import dataclass
from sklearn import mixture
from astropy import table

@dataclass
class GC_Data_Frame:
    '''Class for keeping track of a Globular Cluster'''
    name: str
    mass: float
    total_luminosity: float
    gaussian_fit: sklearn.mixture.gaussian_mixture.GaussianMixture
    Cas: float
    starlist: table.Table
    quantity_on_hand: int = 0

    def write_out(self, file_name):
        #write out to file

    def read_from_file(self, file_name):
        #write out to file



