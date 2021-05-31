import numpy as np
import matplotlib.pyplot as plt
import math

#part a, build a scatterplot of the data
plt.figure(1)
x = np.array([1.1, 1.6, 2.0, 2.1, 2.9, 3.2, 3.3, 4.4, 4.9]) #input x-values
y = np.array([72.61, 72.91, 73.00, 73.11, 73.52, 73.70, 76.10, 74.26, 74.51]) #input y-values
plt.scatter(x, y)

#part b, plot the least squares regression line
mean_x = np.mean(x) #mean of x-data values
mean_y = np.mean(y) #mean of y-data values

#initialize numerator and denominator as 0 in the beginning, for next step
numerator = 0
denominator = 0

#plug in the formula, use for loop in place of sigma to iterate through terms
for i in range(len(x)):
    numerator += (x[i] - mean_x) * (y[i] - mean_y) #numerator of formula
    denominator += (x[i] - mean_x) ** 2 #denominator of formula

slope = numerator/denominator #slope definition
intercept = mean_y - (slope * mean_x) #intercept definition from formula
print('y = ' + str(slope) + 'x + ' + str(intercept))

#because we don't want extrapolation, we need to set a reasonable interval for the linspace
#x-range
x_max = np.max(x) + 1.1
x_min = np.min(x) - 1.1

#get X and Y values for the linear regression line
valuesX = np.linspace(x_min, x_max)
valuesY = intercept + slope * valuesX

#plot the linear regression line
plt.plot(valuesX, valuesY)

#part c, plug in x=3.5; standard deviation in y
#chi squares for standard deviation
top = 0
bottom = 0
for i in range (len(x)):
    top += (y[i] - intercept + slope * x[i])**2
    bottom += intercept + slope * x[i]
chi_square = top/bottom
std = math.sqrt(chi_square/(len(x) - 2))

print(str(slope * 3.5 + intercept) + ' +/- ' + str(std))
#74.13809968847353 +/- 1.0215891759628446

#part d, revise the plot based on the outliers
#(X,Y) = (3.3, 76.10) does not fit the data and is 2 sigma away!
plt.figure(2)
newX = np.array([1.1, 1.6, 2.0, 2.1, 2.9, 3.2, 4.4, 4.9]) #input x-values
newY = np.array([72.61, 72.91, 73.00, 73.11, 73.52, 73.70, 74.26, 74.51]) #input y-values
plt.scatter(newX, newY) #build scatterplot for new data

mean_x = np.mean(newX) #mean of x-data values
mean_y = np.mean(newY) #mean of y-data values


#initialize numerator and denominator as 0 in the beginning, for next step
numerator = 0
denominator = 0

#plug in the formula, use for loop in place of sigma to iterate through terms
for i in range(len(newX)):
    numerator += (newX[i] - mean_x) * (newY[i] - mean_y) #numerator of formula
    denominator += (x[i] - mean_x) ** 2 #denominator of formula

slope = numerator/denominator #slope definition
intercept = mean_y - (slope * mean_x) #intercept definition from formula
print('y = ' + str(slope) + 'x + ' + str(intercept))

#because we don't want extrapolation, we need to set a reasonable interval for the linspace
#x-range
x_max = np.max(newX) + 1.1
x_min = np.min(newX) - 1.1

#get X and Y values for the linear regression line
valuesX = np.linspace(x_min, x_max)
valuesY = intercept + slope * valuesX

#plot the linear regression line
plt.plot(valuesX, valuesY)

#part e, print the new error & value according to new regression
#chi squares for standard deviation
top = 0
bottom = 0
for i in range (len(newX)):
    top += (newY[i] - intercept + slope * newX[i])**2
    bottom += intercept + slope * newX[i]
chi_square = top/bottom
std = math.sqrt(chi_square/(len(newX) - 2))
print(str(slope * 3.5 + intercept) + ' +/- ' + str(std))

#show the plot
plt.show()
