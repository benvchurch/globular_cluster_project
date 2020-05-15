from photutils import aperture_photometry, CircularAperture
import matplotlib
import matplotlib.pyplot as plt
from sklearn import mixture
import numpy as np

def make_hr_diagram(star_list, clust, plot_directory):
    magnitues = [s.tot_mag() for s in star_list]
    colors = [s.BV_col() for s in star_list]
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(12,16))
    plt.xlabel('B-V color')
    plt.xlabel('magnitue')
    plt.title(clust + ' Color Magnitude Diagram')
    plt.plot(colors, magnitues, 'ko')
    fig.savefig(plot_directory + clust + '_HR.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


def make_m_diagram(star_list, clust, plot_directory):
    metal = [s.m1() for s in star_list]
    colors = [s.BV_col() for s in star_list]
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(12,16))
    plt.xlabel('m1 metal abundance index')
    plt.xlabel('B-V color')
    plt.title(clust + ' Metalicity Color Diagram')
    plt.plot(metal, color, 'ko')
    fig.savefig(plot_directory + clust + '_HR.png', dpi=300, bbox_inches='tight')
    plt.close(fig)



def avg_color(star_list):
    print [s.BV_col() for s in star_list]
    return np.mean([s.BV_col() for s in star_list])

def avg_metal(star_list):
    return np.mean([s.m1() for s in star_list])

def fit_cluster_shape(positions):
    clf = mixture.GaussianMixture(n_components=1, covariance_type='full')
    clf.fit(positions)
    centroid = clf.means_[0]
    covariance = clf.covariances_[0]

    eigen_vals = np.linalg.eig(covariance)[0]
    Casp = np.sqrt(abs(eigen_vals[0] - eigen_vals[1])/(eigen_vals[0] + eigen_vals[1]))

    return Casp

# TODO
def fit_cluster(positions, tar_list):

    X_train = [(s.pos[0], s.pos[1], s.m1(), s.BV_col()) for s in star_list]
    clf = mixture.GaussianMixture(n_components=1, covariance_type='full')
    clf.fit(X_train)
