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

def pipeline(inst_sG, inst_sR, wcs, apass, sG, sR, r1, r2):
    hdu2 = fits.open(wcs)
    wcs_head = hdu2[0].header
    wcs = WCS(wcs_head)

    ra, dra, dec, ddec, V, dV, B, dB, sG, dsG, sR, dsR = np.loadtxt(apass, unpack=True, skiprows=1, delimiter=',')

    x_pix, y_pix = wcs. all_world2pix(ra * u.deg, dec * u.deg, 1)
    positions = np.transpose([x_pix, y_pix])

    hdu = fits.open(sG)
    sGdata = np.array(hdu[0].data, dtype = np.int32)

    inst_sG_mag = get_inst_mag(positions, sGdata, r1)

    plt.imshow(Vdata, cmap='gray_r', vmin=0, vmax=2000)
    plt.scatter(x_pix, y_pix, s=10, facecolor='none', lw=3, edgecolors='b')
    plt.show()

    hdu = fits.open(sR)
    sRdata = np.array(hdu[0].data, dtype = np.int32)

    inst_sR_mag = get_inst_mag(positions, sRdata, r2)


    inst_sGsR = inst_sG_mag - inst_sR_mag
    app_sGsR = sG - R
    Vlist = V - inst_v_mag

    #trim out bad data for fitting
    mask = np.isnan(inst_sGsR)
    inst_sGsR = inst_sGsR[~mask]
    app_sGsR = app_sGsR[~mask]
    sGlist = sGlist[~mask]

    mask = (np.abs(inst_sGsR) <= 2)
    inst_sGsR = inst_sGsR[mask]
    app_sGsR = app_sGsR[mask]
    sGlist = sGlist[mask]

    mask = (inst_vr >= -0.5)
    inst_sGsR = inst_sGsR[mask]
    app_sGsR = app_sGsR[mask]
    sGlist = sGlist[mask]

    fit, cov = np.polyfit(inst_sGsR, app_sGsR, 1, cov=True)
    Tgr, Cgr = fit[0], fit[1]
    print(Tgr, Cgr, np.sqrt(np.diag(cov)))

    #fit, cov = np.polyfit(app_sGsR, sGlist, 1, cov=True)
    #Tg, Cg = fit[0], fit[1]
    #print(Tg, Cg, np.sqrt(np.diag(cov)))

    corrected_BV = (inst_sG + Cgr)/1.09




    corrected_VR = Tvr * (inst_sG - inst_sR) + Cvr
    corrected_V = inst_sG_mag + Tv * corrected_VR + Cv
    corrected_R = corrected_V - corrected_VR
    offset = 30
    corrected_V -= offset
    corrected_R -= offset
    print(str(corrected_V))
    print(str(corrected_R))

    print('-------------------------------------')

pipeline(21.663, 20.620, '20200718/20200718sG_wcs.fits', '20200718/20200718sG_apass1.csv', '20200718/20200718sG.fit', '20200718/20200718sR.fit', (5, 8, 10), (5, 8, 10))
pipeline(21.141, 20.224, '20200720/20200720sG_wcs.fits', '20200720/20200720sG_apass1.csv', '20200720/20200720sG.fit', '20200720/20200720sR.fit', (5, 8, 10), (5, 8, 10))
pipeline(19.851, 20.080, '20200721/20200721sG_wcs.fits', '20200721/20200721sG_apass1.csv', '20200721/20200721sG.fit', '20200721/20200721sR.fit', (5, 8, 10), (5, 8, 10))
pipeline(19.923, 19.473, '20200725/20200725sG_wcs.fits', '20200725/20200725sG_apass1.csv', '20200725/20200725sG.fit', '20200725/20200725sR.fit', (5, 8, 10), (5, 8, 10))
pipeline(20.149, 19.664, '20200730/20200730sG_wcs.fits', '20200730/20200730sG_apass1.csv', '20200730/20200730sG.fit', '20200730/20200730sR.fit', (5, 8, 10), (5, 8, 10))
pipeline(20.244, 20.620, '20200804/20200804sG_wcs.fits', '20200804/20200804sG_apass1.csv', '20200804/20200804sG.fit', '20200804/20200804sR.fit', (5, 8, 10), (5, 8, 10))
