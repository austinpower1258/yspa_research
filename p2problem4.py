import math

def convertSexagesimalToDecimal(tuple):
    degrees = tuple[0]
    arcminutes = tuple[1]
    arcseconds = tuple[2]
    sign = 1 #toggle sign
    if (degrees < 0):
        degrees = -degrees #make degrees positive
        sign = -1 #store the sign for later
    #use change of base formula and include sign in product
    comp = sign * (degrees + (arcminutes/60) + (arcseconds/3600))
    return comp #return the computation

def convertDecimalToSexagesimal(decimal):
    sign = 1
    if (decimal < 0): #in the case that the decimal is negative
        sign = -1 #store the sign
        decimal = -decimal #reverse decimal variable (to keep positive)
    degrees = math.trunc(decimal) #whole number is in degrees
    #truncate (remaining x 60) to get arcminutes
    arcminutes = math.trunc((decimal-degrees) * 60)
    #truncate (remaining x 60) to get arcseconds
    arcseconds = round((((decimal-degrees) * 60) - arcminutes) * 60)
    degrees *= sign #add the initial sign to the degrees portion of tuple
    return (degrees, arcminutes, arcseconds); #return tuple

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

    return sidereal_time

#retrieves the JD of given LST
def retrieve():
    notFound = True #if target is not found, keep running
    JD = 2459043.66667
    while(notFound):
        #we want the LST: 10:16:04... longitude is -149.06 degrees
        if ((10, 16, 4) == realJulianDayNumberToLST(JD, -149.06)):
            notFound = False #stop running the while loop
            return JD
        JD +=  0.00001 #increment (for precision purposes)

#base-60 data
leitner_lat = (41, 18, 0)
leitner_long = (-72, 56, 0)
nm_lat = (32, 53, 0)
nm_long = (-105, 29, 0)
ss_lat = (-31, 17, 0)
ss_long = (149, 4, 0)
supernova_ra = (10, 16, 4)
supernova_d = (-60, 32, 52)

#time
sidereal_time_diff = (8, 22, 8)
sidereal_time_decimal = convertSexagesimalToDecimal(sidereal_time_diff)
local_time = (366.25/365.25) * sidereal_time_decimal
local_time_60 = convertDecimalToSexagesimal(local_time)
print("{:02d}:{:02d}:{:02d}".format(local_time_60[0], local_time_60[1], local_time_60[2]))


#print base-60 data in base-10
print(convertSexagesimalToDecimal(leitner_lat))
print(convertSexagesimalToDecimal(leitner_long))
print(convertSexagesimalToDecimal(nm_lat))
print(convertSexagesimalToDecimal(nm_long))
print(convertSexagesimalToDecimal(ss_lat))
print(convertSexagesimalToDecimal(ss_long))
print(convertSexagesimalToDecimal(supernova_ra))
print(convertSexagesimalToDecimal(supernova_d))
print(retrieve()) #retrieves Julian Day Number: 2459044.5298165726
