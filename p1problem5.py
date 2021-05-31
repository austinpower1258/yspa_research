#Austin Wang, July 1, 2020
#Problem 5 of Problem Set 1

import matplotlib.pyplot as plt #import to use plot functions
import matplotlib.patches as mpatches #import to add to labels/colors to legend

#days numbered
days =(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
        18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)

#monthly temperature dataset from Irvine
temperature = (82, 80, 88, 73, 71, 73, 75, 91, 96, 93, 87, 75, 76,
                77, 75, 75, 73, 73, 76, 78, 77, 77, 78, 77, 76, 78,
                77, 73, 75, 76)

#plot figure 1, differentiate from challenge problem
plt.figure(1)
plt.plot(days, temperature, 'bo') #plot temperature vs. days w/ blue dots
plt.xlabel('Day Number in June') #x-axis label
plt.ylabel('Temperature (F)') #y-axis label
plt.title('June Weather in Irvine, California') #title name
plt.axis([0, 31, 70, 100]) #give range and domain of plot

#diffentiate plot from the original problem's plot
plt.figure(2)
plt.xlabel('Day Number in June') #x-axis label
plt.ylabel('Temperature (F)') #y-axis label
plt.title('June High/Low Weather in Irvine, California') #title name

#historical high temp from Irvine
high = [89, 92, 92, 94, 97, 91, 91, 91, 106, 109, 103, 106, 98,
        104, 104, 105, 101, 102, 102, 103, 100, 100, 96, 97, 101,
        103, 106, 105, 96, 101]

#historical low temp from Irvine
low = [41, 40, 40, 44, 42, 41, 43, 40, 43, 42, 42, 41, 42,
        45, 44, 43, 43, 44, 44, 46, 45, 48, 49, 45, 45, 44, 46,
        47, 45, 46]

#colors, gathered from dataset - used legend
palette = ['purple', 'green', 'yellow', 'black', 'black', 'yellow',
          'orange', 'orange', 'orange', 'orange', 'yellow', 'orange', 'yellow',
          'orange', 'purple', 'purple', 'green', 'green', 'purple', 'black',
          'purple', 'purple', 'purple', 'black', 'purple', 'yellow', 'yellow',
          'black', 'purple', 'black']

#function to find difference between low and high historical temps
def diffBetweenLowHigh(highT, lowT):
    diff = list(range(len(highT)))
    for i in range(len(highT)):
        diff[i] = highT[i] - lowT[i] #subtract historical high - low per day
    return diff #return the array of differences


#start from low temp, add length of diff
diff = diffBetweenLowHigh(high, low) #array of diff for bar segment length
temp = plt.bar(days, diff, color=palette,bottom=low)

#add legend labels
sunny = mpatches.Patch(color='orange', label='Clear') #add sunny legend label
fair = mpatches.Patch(color='yellow', label='Fair') #fair label
partlyCloudy = mpatches.Patch(color='green', label='Partly Cloudy') #partlyCloudy label
mostlyCloudy = mpatches.Patch(color='purple', label='Mostly Cloudy') #mostlyCloudy label
cloudy = mpatches.Patch(color='black', label='Cloudy') #cloudy label
rainy = mpatches.Patch(color='blue', label='Rainy') #rainy label

#add legend with handles, location, dataset
plt.legend(temp, loc='upper right', handles=[sunny, fair, partlyCloudy,
                                            mostlyCloudy, cloudy, rainy])
#plot with specific domain and range
plt.axis([0, 31, 0, 176])

#show the plot
plt.show()
