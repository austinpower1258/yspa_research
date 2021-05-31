import random
import math

#generate an array of n population of people
# 1 denotes infected, 0 denotes healthy
#ratio defines the COVID-infected rate
def generateSampleCases(ratio, population):
    list = [];
    infectedNumber = int(ratio * population)
    healthyNumber = int((1 - ratio) * population)
    #in order to insert a ratio of infected people
    for i in range (0, infectedNumber):
        list.append(1)
    #in order to insert a ratio of healthy people
    for j in range (0, healthyNumber):
        list.append(0)

    #shuffles the list to random order
    random.shuffle(list)
    return list

#generate the array
cases = generateSampleCases(0.01, 2195)

#print the cases
print(cases)

#declare a variable reagants (number of reagants)

reagants = 0

def poolTesting(people):
    positive = False
    #in recursive functions, we need to store a global variable
    #we cannot initialize it inside the function
    global reagants

    #increment reagants everytime the function is run
    #since this is recursive
    reagants += 1

    #since we are branching by 2, we need to initialize 2 arrays
    group1 = []
    group2 = []

    #check to see if there are infected people in the groups
    if (len(people) != 1):
        for x in range(len(people)):
            if (people[x] == 1):
                positive = True

    #if there are infected people and the array length is greater than 1
    if (positive and len(people) >= 1):
        for i in range(0, int(len(people)/2)):
            group1.append(people[i])
        #branch out the recursion
        poolTesting(group1)

        #likewise for the second branch of groups
        for j in range(int(len(people)/2), int(len(people))):
            group2.append(people[j])

        poolTesting(group2)
    #return reagants at the end - should give us our answer
    return reagants

print(poolTesting(cases))
