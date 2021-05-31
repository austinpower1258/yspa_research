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

def get_inst_mag(pos, data, r):
    r_c = r[0]
    r_in = r[1]
    r_out = r[2]
    star = CircularAperture(pos, r=r_c)
    bkgd = CircularAnnulus(pos, r_in = r_in, r_out = r_out)
    apers = [star, bkgd]
    phot_table = aperture_photometry(data, apers, method='exact')
    bkgd_flux = phot_table['aperture_sum_1']/bkgd.area*star.area
    flux = phot_table['aperture_sum_0'] - bkgd_flux
    mag = -2.5 * np.log10(flux)
    return mag

def pipeline(inst_sG, inst_sR, wcs, apass, inst_v, inst_r, r1, r2):
    hdu2 = fits.open(wcs)
    wcs_head = hdu2[0].header
    wcs = WCS(wcs_head)

    ra, dra, dec, ddec, V, dV, R, dR = np.loadtxt(apass, unpack=True, skiprows=1, delimiter=',')

    x_pix, y_pix = wcs. all_world2pix(ra * u.deg, dec * u.deg, 1)
    positions = np.transpose([x_pix, y_pix])

    hdu = fits.open(inst_v)
    Vdata = np.array(hdu[0].data, dtype = np.int32)

    inst_v_mag = get_inst_mag(positions, Vdata, r1)

    #plt.imshow(Vdata, cmap='gray_r', vmin=0, vmax=2000)
    #plt.scatter(x_pix, y_pix, s=10, facecolor='none', lw=3, edgecolors='b')
    #plt.show()

    hdu = fits.open(inst_r)
    Rdata = np.array(hdu[0].data, dtype = np.int32)

    inst_r_mag = get_inst_mag(positions, Rdata, r2)


    inst_vr = inst_v_mag - inst_r_mag
    app_vr = V - R
    Vlist = V - inst_v_mag

    #trim out bad data for fitting
    mask = np.isnan(inst_vr)
    inst_vr = inst_vr[~mask]
    app_vr = app_vr[~mask]
    Vlist = Vlist[~mask]

    mask = (np.abs(inst_vr) <= 2)
    inst_vr = inst_vr[mask]
    app_vr = app_vr[mask]
    Vlist = Vlist[mask]

    mask = (inst_vr >= -0.5)
    inst_vr = inst_vr[mask]
    app_vr = app_vr[mask]
    Vlist = Vlist[mask]

    fit, cov = np.polyfit(inst_vr, app_vr, 1, cov=True)
    Tvr, Cvr = fit[0], fit[1]
    print(Tvr, Cvr, np.sqrt(np.diag(cov)))

    plt.figure(1)
    plt.scatter(inst_vr, app_vr, V-R)
    xlist = np.linspace(-0.5, 2, 100)
    ylist = Tvr * xlist + Cvr
    plt.title('Least Square Regression')
    plt.xlabel('Instrumental v - r')
    plt.ylabel('Standard Apparent V - R')
    plt.plot(xlist, ylist, label='y = ' + str(round(Tvr, 4)) +'x + ' + str(round(Cvr, 4)))
    plt.legend(loc='upper left')
    plt.show()


    fit, cov = np.polyfit(app_vr, Vlist, 1, cov=True)
    Tv, Cv = fit[0], fit[1]
    print(Tv, Cv, np.sqrt(np.diag(cov)))


    corrected_VR = Tvr * (inst_sG - inst_sR) + Cvr
    corrected_V = inst_sG + Tv * corrected_VR + Cv
    corrected_R = corrected_V - corrected_VR
    offset = 30
    corrected_V -= offset
    corrected_R -= offset
    print(str(corrected_V))
    print(str(corrected_R))

    print('-------------------------------------')

pipeline(21.663, 20.620, '20200718/20200718sG_wcs.fits', '20200718/20200718sG_apass.csv', '20200718/20200718sG.fit', '20200718/20200718sR.fit', (5, 8, 10), (5, 8, 10))
pipeline(21.141, 20.224, '20200720/20200720sG_wcs.fits', '20200720/20200720sG_apass.csv', '20200720/20200720sG.fit', '20200720/20200720sR.fit', (5, 8, 10), (5, 8, 10))
pipeline(19.851, 20.080, '20200721/20200721sG_wcs.fits', '20200721/20200721sG_apass.csv', '20200721/20200721sG.fit', '20200721/20200721sR.fit', (5, 8, 10), (5, 8, 10))
pipeline(19.923, 19.473, '20200725/20200725sG_wcs.fits', '20200725/20200725sG_apass.csv', '20200725/20200725sG.fit', '20200725/20200725sR.fit', (5, 8, 10), (5, 8, 10))
pipeline(20.149, 19.664, '20200730/20200730sG_wcs.fits', '20200730/20200730sG_apass.csv', '20200730/20200730sG.fit', '20200730/20200730sR.fit', (5, 8, 10), (5, 8, 10))
pipeline(20.244, 20.620, '20200804/20200804sG_wcs.fits', '20200804/20200804sG_apass.csv', '20200804/20200804sG.fit', '20200804/20200804sR.fit', (5, 8, 10), (5, 8, 10))

print('T30 ----------------------------')

pipeline(19.505, 19.025, '20200719-T30/20200719R_wcs.fits', '20200719-T30/20200719R_apass.csv', '20200719-T30/20200719V.fit', '20200719-T30/20200719R.fit', (5, 8, 10), (5, 8, 10))
pipeline(20.567, 19.885, '20200805-T30/20200805R_wcs.fits', '20200805-T30/20200805R_apass.csv', '20200805-T30/20200805V.fit', '20200805-T30/20200805R.fit', (5, 8, 10), (5, 8, 10))
