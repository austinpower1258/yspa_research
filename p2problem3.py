#Austin Wang, July 9, 2020
#Problem 3 of Problem Set 2

import math #to use truncate function in math library

#write function to convert Julian Day Number to LST with a given longitude
def realJulianDayNumberToLST(JD, longitude):
    JD_modified = 2457388.5 #reference January 1, 2016
    lst_reference = 6.6725 #derived from LST 06:40:21
    sidereal_days = 1.0027379 * (JD - JD_modified) #convert to sidereal days
    #take the remainder... we don't care about whole number of days
    sidereal_remainder = sidereal_days - math.trunc(sidereal_days)
    #convert to hr time, convert remainder into hr time, take lst ref into account
    #add longitude... divide by 15 since 15 degrees longitude = 1 hr time
    #mod 24 because we want the time (in hr time)
    sidereal_hrtime = (sidereal_remainder * 24 + lst_reference + longitude/15.0) % 24.0
    #convert hr time to base-60 time (standard)
    sidereal_time = convertDecimalToSexagesimal(sidereal_hrtime)
    lst_hr = sidereal_time[0]
    lst_min = sidereal_time[1]
    lst_sec = sidereal_time[2]
    #format the time into a readable string
    lst = "{:02d}:{:02d}:{:02d}".format(lst_hr, lst_min, lst_sec)
    return lst

#helper function to convert from base-10 to base-60 for time
def convertDecimalToSexagesimal(decimal):
    sign = 1
    if (decimal < 0): #in the case that the decimal is negative
        sign = -1 #store the sign
        decimal = -decimal #reverse decimal variable (to keep positive)
    degrees = math.trunc(decimal) #whole number is in degrees
    #truncate (remaining x 60) to get arcminutes
    arcminutes = math.trunc((decimal-degrees) * 60)
    #truncate (remaining x 60) to get arcseconds
    arcseconds =  round(((decimal-degrees) * 60 - arcminutes) * 60)
    degrees *= sign #add the initial sign to the degrees portion of tuple
    return (degrees, arcminutes, arcseconds);

#test case from the astronomy handout
print(realJulianDayNumberToLST(2459044.66667, -72.93)) #18:38:12
#test case from the problem statement
print(realJulianDayNumberToLST(2457570.888889, -72.93)) #23:07:43
