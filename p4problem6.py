import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

#photometry tool

#IDs: [484, 626, 627, 639, 636]
#information... background spot, star centers, etc.
bkgd_x = 16
bkgd_xmax = 32
bkgd_y = 16
bkgd_ymax = 32
radius = 5
center_x = [370, 509, 487, 85, 140]
center_y = [619, 468, 460, 414, 320]

#photometry tool for masterV
hdu=fits.open("masterV.fit")
data=hdu[0].data
plt.imshow(data, cmap='gray_r', vmin= 1300, vmax= 2000)

plt.show()
v = []
for i in range (len(center_x)):
    star = data[center_y[i] - radius:center_y[i] + radius + 1, center_x[i] - radius:center_x[i] + radius + 1]
    bkgd = data[bkgd_y:bkgd_ymax, bkgd_x:bkgd_xmax]
    bg = np.mean(bkgd)
    sub_star = star - bg
    flux = np.sum(sub_star)
    mag = -2.5 * np.log10(flux) + 22.26
    v.append(mag)

#photometry tool for masterB
hdu=fits.open("masterB.fit")
data=hdu[0].data
b = []
for j in range (len(center_x)):
    star = data[center_y[j] - radius:center_y[j] + radius + 1, center_x[j] - radius:center_x[j] + radius + 1]
    bkgd = data[bkgd_y:bkgd_ymax, bkgd_x:bkgd_ymax]
    bg = np.mean(bkgd)
    sub_star = star - bg
    flux = np.sum(sub_star)
    mag = -2.5 * np.log10(flux) + 22.26
    b.append(mag)

#photometry tool for masterR
hdu=fits.open("masterR.fit")
data=hdu[0].data
r = []
for k in range (len(center_x)):
    star = data[center_y[k] - radius:center_y[k] + radius + 1, center_x[k] - radius:center_x[k] + radius + 1]
    bkgd = data[bkgd_y:bkgd_ymax, bkgd_x:bkgd_ymax]
    bg = np.mean(bkgd)
    sub_star = star - bg
    flux = np.sum(sub_star)
    mag = -2.5 * np.log10(flux) + 22.26
    r.append(mag)


#From Landolt Equatorial Standard
V = np.array([11.31, 13.47, 13.35, 14.20, 14.87])
#link B-V
BminusV = np.array([1.24, 1.00, 0.78, 0.64, 0.75])
#link V-R
VminusR = np.array([0.66, 0.60, 0.47, 0.40, 0.43])
#find B
B = BminusV + V

#calculated instrumental colors
v = np.array(v)
b = np.array(b)
r = np.array(r)
bminusv = b - v
vminusr = v - r

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

#plotting 1st equation from handout
plt.figure(1)
Tbv = findm(bminusv, BminusV)
Cbv = findb(bminusv, BminusV)
print('Tbv: ' + str(Tbv) + ", Cbv: " + str(Cbv))
plt.scatter(bminusv, BminusV, color="b")
plt.plot([min(bminusv), max(bminusv)], [Tbv*min(bminusv)+Cbv, Tbv*max(bminusv)+Cbv],color="r")
plt.xlabel("b-v")
plt.ylabel("B-V")
plt.title("Standard vs. Instrumental Color")
fig = plt.gcf()
fig.set_size_inches(6, 7)

#plotting 2nd equation from handout
plt.figure(2)
Tvr = findm(vminusr, VminusR)
Cvr = findb(vminusr, VminusR)
print('Tvr: ' + str(Tvr) + ", Cvr: " + str(Cvr))
plt.scatter(vminusr, VminusR, color="b")
plt.plot([min(vminusr), max(vminusr)], [Tvr*min(vminusr)+Cvr, Tvr*max(vminusr)+Cvr],color="r")
plt.xlabel("v-r")
plt.ylabel("V-R")
plt.title("Standard vs. Instrumental Color")
fig = plt.gcf()
fig.set_size_inches(6, 7)

#plotting 3rd equation from handout
plt.figure(3)
Tb = findm(BminusV, B - b)
Cb = findb(BminusV, B - b)
print('Tb: ' + str(Tb) + ", Cb: " + str(Cb))
plt.scatter(BminusV, B - b, color='b')
plt.plot([min(BminusV), max(BminusV)], [Tb*min(BminusV)+Cb, Tb*max(BminusV)+Cb], color='r')
plt.xlabel("B-V")
plt.ylabel("B-b")
plt.title("Difference in B vs. Standard Color")
fig=plt.gcf()
fig.set_size_inches(6, 7)


plt.figure(4)
Tv = findm(VminusR, V - v)
Cv = findb(VminusR, V - v)
print('Tv: ' + str(Tv) + ", Cv: " + str(Cv))
plt.scatter(VminusR, V - v, color='b')
plt.plot([min(VminusR), max(VminusR)], [Tv*min(VminusR)+Cv, Tv*max(VminusR)+Cv], color='r')
plt.xlabel("V-R")
plt.ylabel("V-v")
plt.title("Difference in V vs. Standard Color")
fig=plt.gcf()
fig.set_size_inches(6, 7)

plt.show()
