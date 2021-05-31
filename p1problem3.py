#Austin Wang, June 30, 2020
#Problem 3 of Problem Set 1

import math #imported in order to use math.trunc()

#write a function that will convert base-60 to base-10
def convertSexagesimalToDecimal(degrees, arcminutes, arcseconds):
    sign = 1 #toggle sign
    if (degrees < 0):
        degrees = -degrees #make degrees positive
        sign = -1 #store the sign for later
    #use change of base formula and include sign in product
    comp = sign * (degrees + (arcminutes/60) + (arcseconds/3600))
    return comp #return the computation

#write a function that will convert base-10 to base-60
def convertDecimalToSexagesimal(decimal):
    sign = 1
    if (decimal < 0): #in the case that the decimal is negative
        sign = -1 #store the sign
        decimal = -decimal #reverse decimal variable (to keep positive)
    degrees = math.trunc(decimal) #whole number is in degrees
    #truncate (remaining x 60) to get arcminutes
    arcminutes = math.trunc((decimal-degrees) * 60)
    #truncate (remaining x 60) to get arcseconds
    arcseconds = (((decimal-degrees) * 60) - arcminutes) * 60
    degrees *= sign #add the initial sign to the degrees portion of tuple
    return (degrees, arcminutes, arcseconds); #return tuple

#testing convertSexagesimalToDecimal()
print('Testing convertSexagesimalToDecimal()')
print(convertSexagesimalToDecimal(11, 54, 0)) #returns 11.9
print(convertSexagesimalToDecimal(-60, 31, 10)) #returns -60.519444444444446
print(convertSexagesimalToDecimal(-8, 45, 15.94)) #returns -8.754427777777778
print(convertSexagesimalToDecimal(45, 19, 0))
print(convertSexagesimalToDecimal(149, 4, 0))

#testing convertDecimalToSexagesimal()
print('Testing convertDecimalToSexagesimal()')
print(convertDecimalToSexagesimal(60.04)) #returns (60, 2, 23.99999999999693)
print(convertDecimalToSexagesimal(89.99999)) #returns (89, 59, 59.96399999998857)
print(convertDecimalToSexagesimal(-23.43715)) #returns (-23, 26, 13.739999999996542)
