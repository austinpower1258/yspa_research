import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from matplotlib.colors import LogNorm

def load_fits(fname):
    #load the fits file into python
    hdu = fits.open(fname)
    data = hdu[1].data #accesses the data table
    return data

sfr_full = load_fits('gal_totsfr_dr7_v5_2.fits')
mass_full = load_fits('totlgm_dr7_v5_2b.fit')
z_full = load_fits('gal_fiboh_dr7_v5_2.fits')


print(sfr_full.columns)

#find restrictions
restrictions = np.where((sfr_full['AVG'] > -99) & (mass_full['AVG'] != -1) & (z_full['AVG'] > -99.9))[0]

#print usable
print(len(sfr_full['Avg']) - len(restrictions))

sfr = np.array(sfr_full[restrictions])
mass = np.array(mass_full[restrictions])
z = np.array(z_full[restrictions])

print(sfr)

sfrs = sfr['AVG']
masses = mass['AVG']
metallicities = z['AVG']

print(sfrs)

def plot_mass_vs_metal(masses,metallicities):
    #Plot mass against metalicity.
    plt.hist2d(masses, metallicities, bins=300, norm=LogNorm())
    plt.colorbar()
    plt.title('Mass/Metallicity relation for SDSS Galaxies')
    plt.xlabel(r'log Mass [$M_\odot$]')
    plt.ylabel(r'log Gas Phase Metallicities')
    plt.show()

plot_mass_vs_metal(masses,metallicities)

def plot_sfr_metal(sfrs,metallicities):
    plt.hist2d(sfrs, metallicities, bins=300, norm=LogNorm())
    plt.title('SFR/Metallicity relation for SDSS Galaxies')
    plt.colorbar()
    plt.xlabel(r'log SFR')
    plt.ylabel(r'log Gas Phase Metallicities')
    plt.show()

def plot_mass_sfr(masses=masses,sfrs=sfrs):
    plt.hist2d(masses, sfrs, bins=300, norm=LogNorm())
    plt.title('Mass/SFR relation for SDSS Galaxies')
    plt.colorbar()
    plt.xlabel(r'log Mass')
    plt.ylabel(r'log SFR')
    plt.show()

plot_sfr_metal(sfrs, metallicities)
plot_mass_sfr()

def mass_bins(masses):
    bins = np.linspace(7,12,10)
    binned_masses = []
    binned_sfrs = []
    binned_z = []
    for i in range(len(bins)-1):
        mass_indices = np.where((masses > bins[i]) & (masses < bins[i+1]))[0] #check "where" masses are > left edge of bin and < right edge of bin
        mass_indices = np.array(mass_indices)
        masses_needed = masses[mass_indices] #index masses for the indices found above
        sfr_needed = sfrs[mass_indices] #ditto for sfrs
        z_needed = metallicities[mass_indices] #ditto for metallicities
        binned_masses.append(masses_needed)
        binned_sfrs.append(sfr_needed)
        binned_z.append(z_needed)
    return binned_masses, binned_sfrs, binned_z

def sfr_bins(sfrs):
    bins = np.linspace(-2,2,10)
    binned_masses = []
    binned_sfrs = []
    binned_z = []
    for i in range(len(bins)-1):
        sfr_indices = np.where((sfrs < bins[i + 1]) & (sfrs > bins[i]))[0]
        to_choose = np.array(sfr_indices)
        masses_needed = masses[to_choose] #same process as above
        sfr_needed = sfrs[to_choose]
        z_needed = metallicities[to_choose]
        binned_masses.append(masses_needed)
        binned_sfrs.append(sfr_needed)
        binned_z.append(z_needed)
    return binned_masses, binned_sfrs, binned_z

def z_bins(metallicities):
    bins = np.linspace(8,9.5,10)
    binned_masses = []
    binned_sfrs = []
    binned_z = []
    for i in range(len(bins)-1):
        z_indices = np.where((metallicities < bins[i + 1]) & (metallicities > bin[i]))[0]
        to_choose = np.array(z_indices)
        masses_needed = masses[to_choose] #and once more (but for z)
        sfr_needed = sfrs[to_choose]
        z_needed = metallicities[to_choose]
        binned_masses.append(masses_needed)
        binned_sfrs.append(sfr_needed)
        binned_z.append(z_needed)
    return binned_masses, binned_sfrs, binned_z

def plot_mbins(masses=masses):
    m,s,z = mass_bins(masses)
    for i in range(len(m)):
        plt.hist2d(s[i], z[i], bins=100, norm=LogNorm()) #2d histogram, think about what to index here
        plt.xlabel('Log SFR')
        plt.ylabel('Log Metallicity')
        plt.colorbar()
        plt.figure()
    plt.show()
    return

def plot_sfrbins(sfrs=sfrs):
    m,s,z = sfr_bins(sfrs)
    for i in range(len(m)):
        plt.hist2d(m[i], z[i], bins=100, norm=LogNorm()) #2d histogram, think about what to index here
        plt.xlabel('Log Mass')
        plt.ylabel('Log Metallicity')
        plt.colorbar()
        plt.figure()
    plt.show()
    return

def plot_zbins(metallicities=metallicities):
    m,s,z = z_bins(metallicities)
    for i in range(len(m)):
        plt.hist2d(m[i], s[i], bins=100, norm=LogNorm()) #2d histogram, think about what to index here
        plt.xlabel('Log Mass')
        plt.ylabel('Log SFR')
        plt.colorbar()
        plt.figure()
    plt.show()
    return

plot_mbins()
plot_sfrbins()
plot_zbins()
