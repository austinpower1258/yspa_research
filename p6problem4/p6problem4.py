import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

#load the files
days, absmag = np.loadtxt('TypeIa_days_abs.txt', unpack=True, skiprows=1, delimiter=' ')
mydays, myapp_g, myapp_r = np.loadtxt("p6problem4.csv", unpack=True, skiprows=1, delimiter=',', dtype='float')

def generateLightcurve(mydays, myappmag, days, absmag, title):
    #intialize distance_modulus as 0
    distance_modulus = 0

    #estimate horizontal shift - not doing horizontal fitting
    mydays = mydays - 2459044

    #adjust the abs mags based on distance modulus, initialize
    myabsmags = myappmag - distance_modulus

    #interpolate the data
    model_abs = interp1d(days, absmag, kind='cubic')

    #initialize the variables
    residuals = model_abs(mydays) - myabsmags
    rms = np.sqrt(np.sum(residuals * residuals))

    #initialize delta_rms and delta_distance_modulus
    delta_rms = 1
    delta_distance_modulus = +0.5

    #while loop to recalculate distance modulus and lower residuals
    while (abs(delta_rms) > 1.0e-64):
        old_rms = rms
        distance_modulus += delta_distance_modulus
        myabsmags = myappmag - distance_modulus
        residuals = model_abs(mydays) - myabsmags
        rms = np.sqrt(np.sum(residuals * residuals))
        delta_rms = old_rms - rms
        if (delta_rms < 0.0):
            delta_distance_modulus *= -0.5
    print(distance_modulus)

    #plot our points with the lightcurve model with labeling axis and title
    plt.figure(1)
    x = np.linspace(min(days), max(days), num=1000)
    y = model_abs(x)
    plt.plot(x, y, color='blue')
    plt.scatter(mydays, myabsmags, color='red')
    plt.ylim(max(absmag), min(absmag))
    plt.title(title)
    plt.xlabel("Days since peak")
    plt.ylabel("Absolute Magnitude")
    plt.show()

#generate the lightcurves for each of the filters
generateLightcurve(mydays, myapp_g, days, absmag, "Sloan G Lightcurve")
generateLightcurve(mydays, myapp_r, days, absmag, "Sloan R Lightcurve")
