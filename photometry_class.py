from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

hdu=fits.open("veil_comb_lum.fit")
print(hdu.info()) #get information of the image

data=hdu[0].data
print(data)

plt.figure(1)
plt.imshow(data, origin='lower', cmap='gray_r', vmin= 1200, vmax= 1700)
#plt.colorbar()

plt.figure(2)
plt.hist(data.flat, 50, (0, 5000))
#plt.show()

background_xmin = 45
background_xmax = 50
background_ymin = 190
background_ymax = 195
#sky = data[background_ymin:background_ymax+1, background_xmin:background_xmax+1]
#sky_bkgd = np.mean(sky)
#bkgd_subtracted = data - sky_bkgd



radius = 10
x = 124
y = 265

sky_bkgd = data[y-2*radius:y+2*radius + 1, x- 2*radius:x+2*radius+1]
star = data[y-radius:y+radius+1,x-radius:x-radius+1]
sky = np.mean(sky_bkgd)
sky_flux = np.sum(sky_bkgd)
star_flux = np.sum(star)
scale_factor =  radius**2/((radius*2)**2 - (radius)**2)
sky_flux_scaled = sky_flux * scale_factor
flux = star_flux - sky_flux_scaled


print(flux)
offset = 30
mag = -2.5*np.log10(flux)+offset
print(mag)
