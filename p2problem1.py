import math

#write a function that will convert base-60 to base-10
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

#helper function to convert from decimal degrees to radians
def convertToRadians(decimal):
    return (2 * math.pi/360) * decimal

#function to calculate angular separation between stars
def calculateAngularSeparation(ra1, d1, ra2, d2):
    #converting all units to radians
    ra1_decimal = convertSexagesimalToDecimal(ra1)
    ra2_decimal = convertSexagesimalToDecimal(ra2)
    d1_decimal = convertSexagesimalToDecimal(d1)
    d2_decimal = convertSexagesimalToDecimal(d2)
    ra1_radians = convertToRadians(360 * ra1_decimal/24)
    ra2_radians = convertToRadians(360 * ra2_decimal/24)
    d1_radians = convertToRadians(d1_decimal)
    d2_radians = convertToRadians(d2_decimal)

    #apply the Angular Separation Formula & convert from radians to degrees
    theta = (180/math.pi) * math.acos((math.sin(d1_radians)*math.sin(d2_radians) +
            math.cos(d1_radians)*math.cos(d2_radians)*math.cos(ra1_radians-ra2_radians)))
    return convertDecimalToSexagesimal(theta) #convert answer to base 60

#Star Data
altair_ra = (19, 51, 0)
altair_d = (8, 52, 0)
vega_ra = (18, 37, 0)
vega_d = (38, 47, 0)
deneb_ra = (20, 41, 0)
deneb_d = (45, 19, 0)
# Altair and Vega: (34, 12, 48)
print(calculateAngularSeparation(altair_ra, altair_d, vega_ra, vega_d))
# Vega and Deneb: (23, 45, 51)
print(calculateAngularSeparation(vega_ra, vega_d, deneb_ra, deneb_d))
# Altair and Deneb: (38, 0, 35)
print(calculateAngularSeparation(altair_ra, altair_d, deneb_ra, deneb_d))
