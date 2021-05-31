import numpy as np
import random
import matplotlib.pyplot as plt

#Q1 & 2
plt.figure(1)
noise = np.random.normal(1300, 10, (5, 5))
noise[2][2] += 180
sky = noise
star = sky[2][2]
bkgd = np.delete(sky, 12)
bg = np.median(bkgd)
flux = star - bg
SNR = flux/(4 * np.std(bkgd))
print(SNR)
plt.imshow(noise, cmap='gray_r', interpolation='none')

#Q3
sky = np.zeros((5, 5))
#I predict that the SNR would be around 10.
for n in range(10):
    #generate random image
    noiseArr = np.random.normal(1300, 10, (5, 5))
    noiseArr[2][2] += 180

    #load the image
    sky += noiseArr

    #star is the central square
    star = sky[2][2]

    #delete central square => background
    bkgd = np.delete(sky, 12)

    #take the median
    bg = np.median(bkgd)

#get flux
flux = star - bg

#get signal to noise ratio
noise = 4 * np.std(noiseArr)
snr = flux/noise

print(snr)

#Q4
snrlist = []
sky = np.zeros((5, 5))
for n in range(100):
    noiseArr = np.random.normal(1300, 10, (5, 5))
    #doing the conversion, nets me around 28 electrons for 60 second exposure
    noiseArr[2][2] += 28

    #load the image
    sky += noiseArr
    sky -= np.median(sky)
    #star is the central square
    flux = sky[2][2]
    #delete central square => background
    bkgd = np.delete(sky, 12)

    #get signal to noise ratio
    noise = 4 * np.std(bkgd)
    snr = flux/noise
    snrlist.append(snr)

print(snrlist)

#Q5
plt.figure(2)

def function(x):
    a = 0.75
    return a * np.sqrt(x)

x = np.arange(1, 100)
plt.title("SNR vs. Number of Exposures")
plt.ylabel("SNR")
plt.xlabel("Number of Exposures")
plt.legend()
plt.plot(list(range(1,101)), snrlist, 'b')
plt.plot(x, function(x), 'r')
plt.savefig('stats.png')
plt.show()
