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
