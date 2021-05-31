from astropy.io import fits
from astropy.stats import sigma_clipped_stats
import astropy.units as units
from astropy.wcs import WCS
from photutils import DAOStarFinder, CircularAperture, CircularAnnulus, aperture_photometry
import numpy as np
import matplotlib.pyplot as plt

hdu = fits.open("veil_comb_red.fit")
data = hdu[0].data
hdu2 = fits.open("veil_wcs.fits")
wcs_head = hdu2[0].header
wcs=WCS(wcs_head)

ra,dec,g,r = np.loadtxt("veil_comb_red.csv",unpack=True,skiprows=1,delimiter=',')

x_pix, y_pix = wcs.all_world2pix(ra*u.deg, dec*u.deg, 1)

#print(ra)

#plt_size = 16-g
#plt.scatter(ra, dec, s=plt_size)
#plt.show()

star = CircularAperture(zip(x_pix, y_pix)), r=5)
bkgd = CircularAnnulus(zip(x_pix, y_pix), r_in=7, r_out=9)
apers = [star, bkgd]
phot_table = aperture_photometry(data,apers)
#for col in phot_table.colnames(data,apers)
#    phot_table[col].info.format = '%.4g'
#print(phot_table)

bkgd_flux = phot_table['aperture_sum_1']/bkgd.area*star.area
flux_r = phot_table['aperture_sum_0']-bkgd_flux
inst_r_mag = 2.5 * np.log10(flux_r)
plt.scatter(inst_r_mag, r)
plt.xlabel("instrumental r")
plt.ylabel("apparent r")
plt.show()

hdu=fits.open("veil_comb_green.fit")
data = hdu[0].data

bkgd_flux = phot_table['aperture_sum_1']/bkgd.area*star.area
flux_g = phot_table['aperture_sum_0']-bkgd_flux
inst_g_mag = 2.5 * np.log10(flux_g)
plt.scatter(inst_g_mag, g)
plt.xlabel("instrumental g")
plt.ylabel("apparent g")
plt.show()

plt.scatter(inst_g_mag - inst_r_mag, g-r)
plt.show()

inst_gr = inst_g_mag-inst_r_mag
app_gr = g-r
glist = g-inst_g_mag

mask = np.isnan(inst_gr)
inst_gr = inst_gr[~mask]
app_gr = app_gr[~mask]
glist = glist[~mask]

mask=np.abs(inst_gr)<=2
inst_gr = inst_gr[~mask]
app_gr = app_gr[~mask]
glist = glist[~mask]

mask=(inst)gr>=-0.5)
inst_gr = inst_gr[mask]
app_gr=app_gr[mask]
glist = glist[~mask]

#step 1: calculate slope
#m = sum(xi * yi * ybar)/sum(xi^2 - xi * xbar)
avg_inst_gr = np.mean(inst_gr)
avg_app_gr = np.mean(app_gr)
numerator = np.sum(inst_gr*app_gr-inst_gr*avg_app_gr)
denominator = np.sum(inst_gr * inst_gr - inst_gr * avg_gr)
slope = numerator/denominator
intercept = avg_app_gr - slope * avg_inst_gr

print(slope, intercept)

plt.scatter(inst_gr, app_gr)
xlist = np.linspace(-0.5, 2, 100)
ylist = slope * xlist + intercept
plt.plot(xlist, ylist, 'k', lw=4)
plt.show()

plt.scatter(app_gr, glist)
xbar = np.mean(app_gr)
ybar = np.mean(glist)
numerator = np.sum(app_gr * glist-app_gr*ybar)
denominator = np.sum(glist*glist-glist*xbar)
slope = numerator/denominator
intercept = ybar-slope*xbar
print(slope, intercept)

plt.scatter(app_gr,glist)
ylist=slope*xlist+intercept
plt.plot(xlist,ylist,'k',lw=4)
plt.show()
