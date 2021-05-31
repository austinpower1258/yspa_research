from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

hdu=fits.open("luminance.fit")
print(hdu.info()) #get information of the image

data = hdu[0].data
print(data)

plt.imshow(data, cmap='gray_r', vmin= 1300, vmax= 2000)
plt.colorbar()
plt.show()

plt.hist(data.flat, 50, (0, 5000))
plt.show()

x=284
y=337

x_bkgd_min = 284
x_bkgd_max = 328+1
y_bkgd_min = 412
y_bkgd_max = 457+1
radius=6

star = data[y-radius:y+radius+1,x-radius:x-radius+1]
bkgd = data[y_bkgd, x_bkgd]
bg = np.mean(bkgd)

sub_star = star - bg

plt.imshow(sub_star)
plt.colorbar()
plt.show()

flux = np.sum(star)
print(flux)
offset = 30
mag = -2.5*np.log10(flux)+offset
print(flux.mag)
