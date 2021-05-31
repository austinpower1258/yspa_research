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

def pipeline(sup_v, sup_R, wcs, apass, inst_v, inst_r, r1, r2):
    hdu2 = fits.open(wcs)
    wcs_head = hdu2[0].header
    wcs = WCS(wcs_head)

    ra, dra, dec, ddec, V, dV, R, dR = np.loadtxt(apass, unpack=True, skiprows=1, delimiter=',')

    x_pix, y_pix = wcs. all_world2pix(ra * u.deg, dec * u.deg, 1)
    positions = np.transpose([x_pix, y_pix])

    hdu = fits.open(inst_v)
    Vdata = np.array(hdu[0].data, dtype = np.int32)

    inst_v_mag = get_inst_mag(positions, Vdata, r1)

    plt.imshow(Vdata, cmap='gray_r', vmin=0, vmax=2000)
    plt.scatter(x_pix, y_pix, s=10, facecolor='none', lw=3, edgecolors='b')
    plt.show()

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

    fit, cov = np.polyfit(app_vr, Vlist, 1, cov=True)
    Tv, Cv = fit[0], fit[1]
    print(Tv, Cv, np.sqrt(np.diag(cov)))

    corrected_VR = Tvr * (sup_v - sup_r) + Cvr
    inst_gr = 1.646 * corrected_VR - 0.139



    corrected_GR = Tvr * (inst_gr) + Cvr
    corrected_G = inst_sG + Tv * corrected_VR + Cv
    corrected_R = corrected_V - corrected_VR
    offset = 30
    corrected_G -= offset
    corrected_R -= offset
    print(str(corrected_G))
    print(str(corrected_R))

    print('-------------------------------------')
