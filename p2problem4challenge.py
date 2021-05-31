import matplotlib.pyplot as plt
import math
import numpy as np

def convertToRadians(degrees):
    return (np.pi/180) * degrees

def convertToDegrees(radians):
    return (180/np.pi) * radians


plt.figure(1)
plt.title('Observing AT2020nfo from Leitner Observatory')
plt.xlabel('HA (in hr)')
plt.ylabel('h (in degrees)')
HA_A = np.arange(0, 24, 0.01)
h_A=convertToDegrees(np.arcsin(np.sin(convertToRadians(41.3)) * np.sin(convertToRadians(-13.831269)) + np.cos(convertToRadians(-13.831269)) * np.cos(convertToRadians(41.3)) * np.cos(HA_A)))
plt.plot(HA_A, h_A, 'k')


plt.figure(2)
plt.title('Observing AT2020nfo from NM Skies Observatory')
plt.xlabel('HA (in hr)')
plt.ylabel('h (in degrees)')
HA_B = np.arange(0, 24, 0.01)
h_B=convertToDegrees(np.arcsin(np.sin(convertToRadians(32.88)) * np.sin(convertToRadians(-13.831269)) + np.cos(convertToRadians(-13.831269)) * np.cos(convertToRadians(32.88)) * np.cos(HA_B)))
plt.plot(HA_B, h_B, 'b')

plt.figure(3)
plt.title('Observing AT2020nfo from Siding Springs Observatory')
plt.xlabel('HA (in hr)')
plt.ylabel('h (in degrees)')
HA_C = np.arange(0, 24, 0.01)
h_C=convertToDegrees(np.arcsin(np.sin(convertToRadians(-31.28)) * np.sin(convertToRadians(-13.831269)) + np.cos(convertToRadians(-13.831269)) * np.cos(convertToRadians(-31.28)) * np.cos(HA_C)))
plt.plot(HA_C, h_C, 'g')



#ran out of time for Altitude vs UTC graph

plt.show()
