# E. Lee, July 23, 2020
# iYSPA Problem Set 1, Question 2
# Written with the purpose of finding the test my strategy to optimize reagent use efficiency

import random

# randomArray(N)
# Function to generate array of 0's and 1's with length N with 2% chance of 1 and 98% chance of 0
# input: N is the desired number of terms
# return: array of 0's and 1's with length N
def randomArray(N):
    array = []
    for x in range(N):
        a = random.randint(1, 50)

        #1/50 probability that a patient actually has the virus
        if (a == 1):
            array.append(1)
        else:
            array.append(0)
    return array

# poolTesting(patients)
# Function to count the number of tests/reagents needed with my strategy
# input: patients is the array of 0's and 1's representing whether the patient has the virus or not
# return: number of tests/reagents used
test = 0
def poolTesting(patients):
    #Defining two subarrays for splitting into three arrays if test is positive (sickPerson = True)
    array1 = []
    array2 = []

    #Initalizing the boolean of the test coming out positive to be false
    sickPerson = False

    #Incrementing the number of tests/reagents used by 1
    global test
    test = test + 1

    #Changed the test coming out positive to be true if someone is sick (1 in array)
    if (len(patients) != 1):
        for x in range(len(patients)):
            if (patients[x] == 1):
                sickPerson = True

    #If someone is sick, that group is split into three gruops and pool tested again
    if (sickPerson and len(patients) >= 1):
        for i in range(0, int(len(patients)/2)):
            array1.append(patients[i])
        poolTesting(array1)

        for j in range(int(len(patients)/2), int(len(patients))):
            array2.append(patients[j])
        poolTesting(array2)
    return test

#Generate random array of 3000, with 1 meaning has virus, and 0 meaning doesn't have virus
patients = randomArray(3000)

#Printing the number of tests/reagents used using my strategy
print(poolTesting(patients))
