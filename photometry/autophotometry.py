from astropy.io import fits
from astropy.stats import sigma_clipped_stats
import astropy.units as u
from astropy.wcs import WCS
from photutils import DAOStarFinder, CircularAperture, CircularAnnulus, aperture_photometry
import numpy as np
import matplotlib.pyplot as plt
import glob
from astropy.table import Table

#get the standard positions
hdu2 = fits.open("NGC436_b_wcs.fits")
wcs_head = hdu2[0].header
wcs=WCS(wcs_head)

ra, dec, V, B = np.loadtxt("NGC436_bMODIFIED1.csv", unpack=True, skiprows=1, delimiter=',')
x_pix, y_pix = wcs.all_world2pix(ra*u.deg, dec*u.deg, 1)

#get inst b
hdu = fits.open("NGC436_bALL_comb.fit")
data = hdu[0].data
#star = CircularAperture(zip(x_pix, y_pix), r=3.5)
#bkgd = CircularAnnulus(zip(x_pix, y_pix), r_in= 5.75, r_out = 7)
star = CircularAperture(zip(x_pix, y_pix), r=6.5)
bkgd = CircularAnnulus(zip(x_pix, y_pix), r_in= 6.95, r_out = 7.25)
apers = [star, bkgd]
phot_table = aperture_photometry(data, apers)
bkgd_flux = phot_table['aperture_sum_1'] / bkgd.area * star.area
flux_b  = phot_table['aperture_sum_0'] - bkgd_flux
inst_b = 2.5 * np.log10(flux_b)

#get inst v
hdu = fits.open("NGC436_vALL_comb.fit")
data = hdu[0].data
apers = [star, bkgd]
phot_table = aperture_photometry(data, apers)
bkgd_flux = phot_table['aperture_sum_1'] / bkgd.area * star.area
flux_v = phot_table['aperture_sum_0'] - bkgd_flux
inst_v = 2.5 * np.log10(flux_v)

#trim out data for bad fitting
inst_bv = inst_b - inst_v
app_bv = B - V
Blist = B - inst_b

#get rid of bad data, use mask
mask = np.isnan(inst_bv)
inst_bv = inst_bv[~mask]
app_bv = app_bv[~mask]
Blist = Blist[~mask]

mask = (np.abs(inst_bv) <= 2)
inst_bv = inst_bv[mask]
app_bv = app_bv[mask]
Blist = Blist[mask]

mask = inst_bv >= -0.5
inst_bv = inst_bv[mask]
app_bv = app_bv[mask]
Blist = Blist[mask]

#find the slope
def findm(xi, yi):
    x = np.mean(xi)
    y = np.mean(yi)
    return ((sum(xi * (yi-y)))/(sum(xi**2-xi*x)))

#find the intercept
def findb(xi, yi):
    m = findm (xi, yi)
    x = np.mean(xi)
    y = np.mean(yi)
    return (y-m*x)

#calcuate tbv and cbv
tbv, cbv = findm(inst_bv, app_bv), findb(inst_bv, app_bv)
print(tbv), print(cbv)

#plot tbv and cbv fit to check it
'''
plt.figure(1)
plt.scatter(inst_bv, app_bv)
xlist = np.linspace(np.min(inst_bv) * 0.8, np.max(inst_bv) * 1.1, 100)
ylist = tbv * xlist + cbv
plt.plot(xlist, ylist, lw=4)
plt.ylim(plt.xlim())
plt.xlabel("b-v")
plt.ylabel("B-V")
'''

#calculate corrected B-V
corrected_BV = tbv * (inst_b - inst_v) + cbv

#calculate tb and cb
tb, cb = findm(app_bv, Blist), findb(app_bv, Blist)
print(tb), print(cb)

#plot tb and cb to check
'''
plt.figure(2)
plt.scatter(app_bv, Blist)
ylist = tb * xlist + cb
plt.plot(xlist, ylist, 'k', lw=4)
plt.xlabel("B-V")
plt.ylabel("B-b")
'''
#calculate corrected V
corrected_B = tb * (corrected_BV) + cb + inst_b
corrected_V = corrected_B - corrected_BV

#isochrone fitting time
#load the dat file to glob => loadtxt, and unique to convert to float
files = glob.glob("Isochrones/yapsi_w_X0p629542_Z0p000458.dat")
print(files)
ssp = np.loadtxt(files[0])
ages = np.unique(ssp[:,0])
i = 1
plt.figure(figsize=(9,6))
for age in ages: #iterate through all of the models
    if not i%3:
        mask = np.where(ssp[:,0]==age)
        single_age_ssp=ssp[mask]
        plt.plot(single_age_ssp[:,7],single_age_ssp[:,5], label=age)
    i+=1
plt.legend() #show legend refering to each graph/model
plt.xlim(-0.5, 2) #set limits for x-axis
plt.ylim(20, -20) #set limits for y-axis

#plot V vs. B-V
#shift the plot to align with the
plt.scatter(corrected_BV, corrected_V - 6.5)

#label the plot for readability
plt.title("NGC436: V vs. B-V Plot")
plt.xlabel("B-V")
plt.ylabel("V")

#show the plot
plt.show()