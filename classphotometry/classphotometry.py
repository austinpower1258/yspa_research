from astropy.io import fits
from astropy.stats import sigma_clipped_stats
import astropy.units as u
from astropy.wcs import WCS
from photutils import DAOStarFinder, CircularAperture, CircularAnnulus, aperture_photometry
import numpy as np
import matplotlib.pyplot as plt

#open instrumental fits file
hdu = fits.open("NGC752-blue.fit")
data = hdu[0].data

#apass download official data
hdu2 = fits.open("NGC752-blue-wcs.fits")
wcs_head = hdu2[0].header
wcs=WCS(wcs_head)

ra, dec, v, b = np.loadtxt("NGC752-blue.csv", unpack=True, skiprows=1, delimiter=',')
x_pix, y_pix = wcs.all_world2pix(ra*u.deg, dec*u.deg, 1)


star = CircularAperture(zip(x_pix, y_pix), r=7)
bkgd = CircularAnnulus(zip(x_pix, y_pix), r_in=8, r_out = 10)
apers = [star, bkgd]
phot_table = aperture_photometry(data, apers)


plt.figure(1)
bkgd_flux = phot_table['aperture_sum_1'] / bkgd.area * star.area
flux_b  = phot_table['aperture_sum_0'] - bkgd_flux
inst_b_mag = 2.5 * np.log10(flux_b)
plt.scatter(inst_b_mag, b)
plt.xlabel("instrumental b")
plt.ylabel("apparent b")


hdu = fits.open("NGC752-green.fit")
data = hdu[0].data
phot_table = aperture_photometry(data, apers)

plt.figure(2)
bkgd_flux = phot_table['aperture_sum_1'] / bkgd.area * star.area
flux_v = phot_table['aperture_sum_0'] - bkgd_flux
inst_v_mag = 2.5 * np.log10(flux_v)
plt.scatter(inst_v_mag, v)
plt.xlabel("instrumental v")
plt.ylabel("apparent v")


inst_bv = inst_b_mag - inst_v_mag
app_bv = b - v

mask = np.isnan(inst_bv)
inst_bv = inst_bv[~mask]
app_bv = app_bv[~mask]

mask = (np.abs(inst_bv) <= 2)
inst_bv = inst_bv[mask]
app_bv = app_bv[mask]

mask = inst_bv >= -0.5
inst_bv = inst_bv[mask]
app_bv = app_bv[mask]

#step 1: calculate slope
avg_inst_bv = np.mean(inst_bv)
avg_app_bv = np.mean(app_bv)
numerator = np.sum(inst_bv * app_bv-inst_bv * avg_app_bv)
denominator = np.sum(inst_bv * inst_bv - inst_bv * avg_inst_bv)
tbv = numerator/denominator
cbv = avg_app_bv - slope * avg_inst_bv

plt.figure(3)
plt.scatter(inst_bv, app_bv, b-v)
plt.xlabel("apparent b - v")
plt.ylabel("instrumental b - v")
xlist = np.linspace(-0.5, 2, 100)
ylist = tbv * xlist + cbv
plt.plot(xlist, ylist)

avg_inst_b = np.mean(inst_b_mag)
avg_app_b = np.mean(b)
numerator = np.sum(inst_b_mag * b-inst_bv * avg_app_bv)
denominator = np.sum(inst_bv * inst_bv * inst_bv * avg_inst_bv)
tbv = numerator/denominator
cbv = avg_app_bv - slope * avg_inst_bv
print(slope)
print(intercept)

plt.figure(4)
plt.scatter(inst_bv, app_bv, b-v)
plt.xlabel("apparent b - v")
plt.ylabel("instrumental b - v")
xlist = np.linspace(-0.5, 2, 100)
ylist = tbv * xlist + cbv
plt.plot(xlist, ylist)

plt.figure(5)
corrected_inst_bv = slope * (inst_bv) + intercept
plt.scatter(corrected_inst_bv, app_bv, b-v)
plt.show()
