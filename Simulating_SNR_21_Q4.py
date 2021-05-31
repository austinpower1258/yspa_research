import matplotlib.pyplot as plt
import numpy as np

SNR_list = []
hundredExposureArray = np.zeros((5,5))
for x in range(200):
    array = np.random.normal(1300,10,(5,5))
    array[2,2] += 28.53
    hundredExposureArray += array
    hundredExposureArray = hundredExposureArray - np.median(hundredExposureArray)
    flux = hundredExposureArray[2,2]
    background = np.delete(hundredExposureArray, 12)
    noise = 4 * np.std(background)
    SNR = flux/noise
    SNR_list.append(SNR)
numExposure = []
for x in range(200):
    numExposure.append(x+1)

plt.plot(numExposure, SNR_list)
plt.xlabel('Number of Exposures')
plt.ylabel('SNR')
plt.show()
#plt.imshow(array, cmap = 'gray', interpolation = 'none')
#plt.show()
