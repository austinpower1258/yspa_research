import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

days, absmag = np.loadtxt('TypeIa_days_abs.txt', unpack=True, skiprows=1, delimiter=' ')

distance_modulus = 33.1

mydays = np.array([3, 5, 10.5, 14.0])
myappmags = np.array([14, 14.1, 14.6, 14.8])

myabsmags = myappmags - distance_modulus


model_abs = interp1d(days, absmag, kind='cubic')


residuals = model_abs(mydays) - myabsmags
rms = np.sqrt(np.sum(residuals * residuals))



delta_rms = 1
delta_distance_modulus = +0.5

while (abs(delta_rms) > 0.01):
    old_rms = rms
    distance_modulus += delta_distance_modulus
    myabsmags = myappmags - distance_modulus
    residuals = model_abs(mydays) - myabsmags
    rms = np.sqrt(np.sum(residuals * residuals))
    delta_rms = old_rms - rms
    if (delta_rms < 0.0):
        delta_distance_modulus *= -0.5




print("Distance Modulus = ", distance_modulus)
print("RMS = ", rms)


x = np.linspace(min(days), max(days), num=1000)
y = model_abs(x)

plt.plot(x, y, color='blue')

plt.scatter(mydays, myabsmags, color='red')
plt.ylim(max(absmag), min(absmag))
plt.show()
