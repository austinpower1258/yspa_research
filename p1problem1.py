#Austin Wang, June 28, 2020
#Problem 1 of Problem Set 1

import math #import the math library in order to use math.pi

#Leibnitz's Formula for pi/4 = 1 - 1/3 + 1/5 - 1/7 + ..., we can see a pattern in the series.
def summation(numberOfTerms): #define function ... only difference is that this series converges to pi/4
    denom = 1 #initialize value of denom from first term
    summation = 0 #initial variable for summation
    for i in range(numberOfTerms): #write a for loop to iterate through the number of terms
        if (i % 2 == 0): #if even, we add the term to the summation
            summation += 1/float(denom) #add term, we must cast denom to float since 1/2 = 0 in python 2.
        else: #if odd, we subtract the term
            summation -= 1/float(denom) #subtract term, we must cast denom to float since 1/2 = 0 in python 2.
        denom += 2 #increment denom by two to account for the 1/1 -> 1/3 -> 1/5 changes in the denominator
    return summation #return our summation

def estimatePi(numberOfTerms): #define function
#since this series converges to pi/4, we need to multiply summation by 4 to estimate pi
    return 4 * summation(numberOfTerms)

#testing with test function
def test(): #comparing with actual values
    #estimate pi/4
    print("The real value of pi/4 is " + str(math.pi/4)) #0.7853981633974483
    print(summation(1)) #returns 1.0
    print(summation(10)) #returns 0.7604599047323508
    print(summation(100)) #returns 0.7828982258896384
    print(summation(1000)) #returns 0.7851481634599485
    print(summation(10000)) #returns 0.7853731633975086
    print(summation(100000)) #returns 0.7853956633974299
    print(summation(1000000)) #returns 0.7853979133974436
    print(summation(10000000)) #returns 0.7853981383974479
    print(summation(100000000)) #returns 0.7853981608973315

    #estimate pi
    print("The real value of pi is " + str(math.pi)) #3.141592653589793
    print(estimatePi(1)) #returns 4.0
    print(estimatePi(10)) #returns 3.04183961893
    print(estimatePi(100)) #returns 3.13159290356
    print(estimatePi(1000)) #returns 3.14059265384
    print(estimatePi(10000)) #returns 3.14149265359
    print(estimatePi(100000)) #returns 3.14158265359
    print(estimatePi(1000000)) #returns 3.14159165359
    print(estimatePi(10000000)) #returns 3.14159255359
    print(estimatePi(100000000)) #returns 3.14159264359

test() #run the test program to compare the values
