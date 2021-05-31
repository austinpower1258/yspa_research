from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from astropy.table import Table
import astropy.units as u
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from photutils import DAOStarFinder, CircularAperture, CircularAnnulus, aperture_photometry
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
import glob

def get_inst_mag(pos, data, r_c = 3, r_in = 4, r_out = 6):
    star = CircularAperture(pos, r=r_c)
    bkgd = CircularAnnulus(pos, r_in = r_in, r_out = r_out)
    apers = [star, bkgd]
    phot_table = aperture_photometry(data, apers)
    bkgd_flux = phot_table['aperture_sum_1']/bkgd.area*star.area
    flux = phot_table['aperture_sum_0'] - bkgd_flux
    mag = -2.5 * np.log10(flux)
    return mag

#get standard positions

hdu2 = fits.open('NGC752-blue-wcs.fits')
wcs_head = hdu2[0].header
wcs = WCS(wcs_head)

ra, dra, dec, ddec, V, dV, B, dB = np.loadtxt('NGC752-blue.csv', unpack=True, skiprows=1, delimiter=',')

x_pix, y_pix = wcs. all_world2pix(ra * u.deg, dec * u.deg, 1)
positions = np.transpose([x_pix, y_pix])

#get V mags

hdu = fits.open('NGC752-green.fit')
Vdata = np.array(hdu[0].data, dtype = np.int32)

inst_v_mag = get_inst_mag(positions, Vdata)

plt.imshow(Vdata, cmap='gray_r', vmin=0, vmax=2000)
plt.scatter(x_pix, y_pix, s=10, facecolor='none', lw=3, edgecolors='b')
plt.show()

#calculate b mags
hdu = fits.open('NGC752-blue.fit')
Bdata = np.array(hdu[0].data, dtype = np.int32)

inst_b_mag = get_inst_mag(positions, Bdata)

#trim out bad data for fitting

inst_bv = inst_b_mag - inst_v_mag
app_bv = B-V
Blist = B - inst_b_mag

mask = np.isnan(inst_bv)
inst_bv = inst_bv[~mask]
app_bv = app_bv[~mask]
Blist = Blist[~mask]

mask = (np.abs(inst_bv) <= 2)
inst_bv = inst_bv[mask]
app_bv = app_bv[mask]
Blist = Blist[mask]

mask = (inst_bv >= -0.5)
inst_bv = inst_bv[mask]
app_bv = app_bv[mask]
Blist = Blist[mask]

#calculate Tbv and Cbv

fit, cov = np.polyfit(inst_bv, app_bv, 1, cov=True)
Tbv, Cbv = fit[0], fit[1]
print(Tbv, Cbv, np.sqrt(np.diag(cov)))

#calculate corrected B-V
corr_bv = Tbv * (inst_b_mag - inst_v_mag) + Cbv

#calculate Tv and Cv
fit, cov = np.polyfit(app_bv, Blist, 1, cov=True)
Tb, Cb = fit[0], fit[1]

#get all stars
mean, median, std = sigma_clipped_stats(Vdata, sigma=3.0)
daofind = DAOStarFinder(fwhm=3.0, threshold=5.*std)
Vsources = daofind(Vdata - median)

mean, median, std = sigma_clipped_stats(Bdata, sigma=3.0)
daofind = DAOStarFinder(fwhm=3.0, threshold=3.*std)
Bsources = daofind(Bdata - median)

sources = Table(names=('x','y'))
dist_sq = 0.5
for vstar in Vsources:
    for bstar in Vsources:
        if ((bstar['xcentroid'] - vstar['xcentroid'])**2 + (bstar['ycentroid'] - vstar['ycentroid'])**2) <= dist_sq:
            sources.add_row([bstar['xcentroid'], bstar['ycentroid']])
print(len(sources))

position = np.transpose([sources['x'], sources['y']])

all_inst_b_mag = get_inst_mag(positions, Bdata)
all_inst_v_mag = get_inst_mag(positions, Vdata)

all_BV = Tbv * (all_inst_b_mag - all_inst_v_mag) + Cbv
all_B = Tv * all_BV + Cb + all_inst_v_mag
all_V = all_B - all_BV

#find distance modulus
plt.figure(1)
isochrone = np.loadtxt('Isochrones/yapsi_w_X0p733138_Z0p016862.dat')
iso = isochrone[isochrone[:,0] == 4]
plt.plot(all_BV, all_V, '.')
plt.xlim(-0.5, 2)
plt.ylim(reversed(plt.ylim()))
plt.show()

plt.figure(2)
filelist = glob.glob('C:/Users/cucko/Desktop/YSPA/python/autoisochrone/Isochrones/yapsi_w_X0p*')
age = 0.2
for f in filelist:
    isochrone_data = Table.read(f, format='ascii')
    mask = np.where(isochrone_data['coll'] == age)
    single_age_isochrone(['col8'], single_age_isochrone['col6'])
plt.ylim(reversed(plt.ylim()))

#First iterate over age to find the cluster ages
mask = (all_V < 14) & (BV < 0.5) & (-0.1 < BV)
xd = BV[mask]
yd = V[mask]

fit = []
isochrone_file = 'Isochrones/yapsi_w_X0p602357_Z0p027643.dat'
isochrone = Table.read(isochrone_file, format='ascii') #open up one of the filelist
ages = np.unique(isochrone['coll'])
for ii, age in enumerate(ages):
    single_age_isochrone = isochrone[isochrone['coll'] == age]

    x = single_age_isochrone['col8']
    y = single_age_isochrone['col6']
    #get the main-sequence part of the isochrone
    for i in range(len(x)):
        try:
            if x[i+1] > x[i]:
                break
        except IndexError:
            i = len(x)
            break
    x = x[:i]
    y = y[:i]
    yoff = np.mean(y) - np.nanmean(yd)
    g = interpolate.interpld(x, y)
    mask ((xd <= np.max(x)) & (xd >= np.min(x)))
    xdm = xd[mask]
    ydm = yd[mask] + yoff
    if len(ydm) == 0:
        chi2 = np.inf
    else:
        chi2 = np.sum((ydm - g(xdm))**2/(len(ydm) - 1))
    fit.append([isochrone_file, age, chi2])
    print('%.2f%% finished' % (100.0 * (ii + 1)/len(ages)))

ichi2min = np.argmin(np.array(fit[:,2])
print('best fit file name | age | chi2/(N-1)')
print(fit[ichi2min])


#now iterate over X and Z and only consider best-fit ages
fit2 = []
age = fit[ichi2min][1]
for ii, f in enumerate(filelist):
    isochrone_data = Table.read(f, format='ascii')
    single_age_isochrone = isochrone_data[isochrone_data['coll'] == age]
    x = single_age_isochrone['col8']
    y = single_age_isochrone['col6']
    for i in range(len(x)):
        try:
            if x[i+1]>x[i]:
                break
            except IndexError:
                i = len(x)
                break
    x = x[:i]
    y = y[:i]
    yoff = np.mean(y) - np.nanmean(yd)
    g = interpolate.interpld(x, y)
    mask = ((xd <= np.max(x)) & (xd >= np.min(x)))
    xdm = xd[mask]
    ydm = yd[mask] + yoff
    if len(ydm) == 0:
        chi2 = np.inf
    else:
        chi2 = np.sum((ydm-g(xdm))**2)/len(ydm)-1)
    parts = f.split('_')
    x, z = float(parts[2][1:].replace('p', '.')), float(parts[3][1:-4].replace('p','.'))
    fit2.append([f, FeH, chi2])
    print("%.2f%% finished" % (100.0 * (ii + 1)/len(filelist)))

ichi2min2 = np.argmin(np.array(fit2)[:,2])
print('best fit file name | [Fe/H] | chi2/(N-1)')
print(fit2[ichi2min2])
"""'''
