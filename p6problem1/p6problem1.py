import numpy as np
import matplotlib.pyplot as plt

date, recordedWeather, conditions, high, low = np.loadtxt("RealWeatherData.csv", unpack=True, delimiter=',', dtype='str')

#part a: ratio of cloudy to clear days
def getRatioOfCloudyToClear(conditions):
    daysClear = 0 #initialize daysClear to 0
    for i in range (0, len(conditions)):
        if (conditions[i] == "Fair"): #increment if "Fair"
            daysClear += 1
        if (conditions[i] == "Sunny"): #increment if "Sunny"
            daysClear += 1
        if (conditions[i] == "Clear"): #increment if "Clear"
            daysClear += 1
    return (len(conditions) - daysClear) / daysClear

print(getRatioOfCloudyToClear(conditions))

#part b
def getBestTime(date, conditions):
    daysClearArr = [] #initialize clearArr as empty array
    for i in range(0, len(conditions) - 28):
        daysClear = 0 #initialize daysClear as 0
        for j in range(0, 28): #try to get a run of 28
            if (conditions[i + j] == "Fair"):
                daysClear += 1
            if (conditions[i + j] == "Sunny"):
                daysClear += 1
            if (conditions[i + j] == "Clear"):
                daysClear += 1
        daysClearArr.append(daysClear) #append # of clear into arr
    daysClearArr = np.array(daysClearArr) #convert to np arr
    #return the max clear days and the dates on which it happens
    return date[np.where(daysClearArr == np.amax(daysClearArr))]

print(getBestTime(date, conditions))
#['July 22. 2015 at 05:36AM' 'July 8. 2019 at 05:26AM']

#part c
def getAverageAnnualTemperature(date, recordedWeather):
    recordedWeather = np.array(recordedWeather)
    annualTemp = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, len(conditions)): #run through all cases
        if ("2012" in date[i]): #separate by year, add temperature
            count[0] += 1 #increment count to count days
            annualTemp[0] += int(recordedWeather[i])
        if ("2013" in date[i]):
            count[1] += 1
            annualTemp[1] += int(recordedWeather[i])
        if ("2014" in date[i]):
            count[2] += 1
            annualTemp[2] += int(recordedWeather[i])
        if ("2015" in date[i]):
            count[3] += 1
            annualTemp[3] += int(recordedWeather[i])
        if ("2016" in date[i]):
            count[4] += 1
            annualTemp[4] += int(recordedWeather[i])
        if ("2017" in date[i]):
            count[5] += 1
            annualTemp[5] += int(recordedWeather[i])
        if ("2018" in date[i]):
            count[6] += 1
            annualTemp[6] += int(recordedWeather[i])
        if ("2019" in date[i]):
            count[7] += 1
            annualTemp[7] += int(recordedWeather[i])
        if ("2020" in date[i]):
            count[8] += 1
            annualTemp[8] += int(recordedWeather[i])
    print(annualTemp)
    print(count)
    annualTemp = np.array(annualTemp)
    count = np.array(count)
    annualAverageTemp = annualTemp/count #find average temp per day
    return annualAverageTemp
print(getAverageAnnualTemperature(date, recordedWeather))
#[35.05 47.93715847 47.24376731 46.47527473 47.51648352 47.54768392
# 47.90410959 47.22404372 47.70093458]

#part d
plt.figure(1)
plt.ylim(46, 48)
plt.title("Is Global Warming A Hoax?")
plt.xlabel("Year")
plt.ylabel("Temperature (in Fahrenheit)")
years = np.array([2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])
annualMorningTemp = getAverageAnnualTemperature(date, recordedWeather)
annualMorningTemp = np.delete(annualMorningTemp, 0)
plt.bar(years, annualMorningTemp, color=('red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown', 'black'))
plt.show()
