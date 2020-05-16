from photutils import aperture_photometry, CircularAperture
import matplotlib
import matplotlib.pyplot as plt
from sklearn import mixture
import numpy as np

def make_hr_diagram(star_list, clust, plot_directory):
    magnitues = [s.tot_mag() for s in star_list]
    colors = [s.BV_col() for s in star_list]
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(12,16))
    plt.xlabel('B-V color', fontsize=16)
    plt.ylabel('magnitue', fontsize=16)
    plt.title(clust + ' Color Magnitude Diagram', fontsize=24)
    plt.plot(colors, magnitues, 'ko')
    fig.savefig(plot_directory + clust + '_HR.pdf', dpi=300, bbox_inches='tight')
    ax.set_xlim(-3,3)
    plt.close(fig)
    
def make_VR_diagram(star_list, clust, plot_directory):
    magnitues = [s.tot_mag() for s in star_list]
    colors = [s.VR_col() for s in star_list]
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(12,16))
    plt.xlabel('V-R color', fontsize=16)
    plt.ylabel('magnitue', fontsize=16)
    plt.title(clust + ' Color Magnitude Diagram', fontsize=24)
    plt.plot(colors, magnitues, 'ko')
    fig.savefig(plot_directory + clust + '_VR.pdf', dpi=300, bbox_inches='tight')
    ax.set_xlim(-3,3)
    plt.close(fig)  
    

def make_BR_diagram(star_list, clust, plot_directory):
    magnitues = [s.tot_mag() for s in star_list]
    colors = [s.BR_col() for s in star_list]
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(12,16))
    plt.xlabel('V-R color', fontsize=16)
    plt.ylabel('magnitue', fontsize=16)
    plt.title(clust + ' Color Magnitude Diagram', fontsize=24)
    plt.plot(colors, magnitues, 'ko')
    fig.savefig(plot_directory + clust + '_BR.pdf', dpi=300, bbox_inches='tight')
    ax.set_xlim(-3,3)
    plt.close(fig)    


def make_BG_diagram(star_list, clust, plot_directory):
    magnitues = [s.tot_mag() for s in star_list]
    colors = [s.BG_col() for s in star_list]
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(12,16))
    plt.xlabel('V-R color', fontsize=16)
    plt.ylabel('magnitue', fontsize=16)
    plt.title(clust + ' Color Magnitude Diagram', fontsize=24)
    plt.plot(colors, magnitues, 'ko')
    fig.savefig(plot_directory + clust + '_BG.pdf', dpi=300, bbox_inches='tight')
    ax.set_xlim(-3,3)
    plt.close(fig)    
      


def make_m_diagram(star_list, clust, plot_directory):
    metal = [s.m1() for s in star_list]
    colors = [s.BV_col() for s in star_list]
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(12,16))
    plt.xlabel('m1 metal abundance index', fontsize=16)
    plt.ylabel('B-V color', fontsize=16)
    plt.title(clust + ' Metalicity Color Diagram', fontsize=24)
    plt.plot(metal, colors, 'ko')
    fig.savefig(plot_directory + clust + '_MC.pdf', dpi=300, bbox_inches='tight')
    plt.close(fig)



def avg_color(star_list):
    return np.log(np.mean([np.exp(s.BV_col()) for s in star_list]))

def avg_metal(star_list):
    return np.log(np.mean([np.exp(s.m1()) for s in star_list]))

def fit_cluster_shape(positions):
    clf = mixture.GaussianMixture(n_components=1, covariance_type='full')
    clf.fit(positions)
    centroid = clf.means_[0]
    covariance = clf.covariances_[0]

    eigen_vals = np.linalg.eig(covariance)[0]
    Casp = np.sqrt(abs(eigen_vals[0] - eigen_vals[1])/(eigen_vals[0] + eigen_vals[1]))

    return Casp

# TODO
def fit_cluster(positions, star_list, image, clust, plot_directory):
	print "HERE"
	X_train = [(s.pos[0], s.pos[1], s.m1(), s.BV_col()) for s in star_list]
	clf = mixture.GaussianMixture(n_components=2, covariance_type='full')
	clf.fit(X_train)
	labels = clf.predict(X_train)
    
	fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(12,16))
	plt.title('Gaussian Mixture Classified Stars')
	maximum = np.quantile(image.flatten(), 0.99)
	plt.imshow(image, cmap='gray', interpolation='nearest', vmin = 0, vmax = maximum)
	
	print set(labels)
	
	for component in range(0,1):
		apertures = CircularAperture([positions[i] for i, l in enumerate(labels) if l == component], r=4.)
		if component == 1:
			star_list_trunc = [star_list[i] for i, l in enumerate(labels) if l == component]
			apertures.plot(color='red', lw=1.5)
		else:
			apertures.plot(color='blue', lw=1.5)

	fig.savefig(plot_directory + clust + '_classified.pdf', dpi=300, bbox_inches='tight')
	plt.close(fig)
	covariance = clf.covariances_[0][0:2, 0:2]

	eigen_vals = np.linalg.eig(covariance)[0]
	Casp = np.sqrt(abs(eigen_vals[0] - eigen_vals[1])/(eigen_vals[0] + eigen_vals[1]))
	return Casp, star_list_trunc

	
