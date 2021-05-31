#Austin Wang, June 29, 2020
#Problem 2 of Problem Set 1

import time #imported for timer function for the average sort time challenge
import random #imported to randomize lists of 10 integers
import copy #imported to deepcopy arrays for the average sort time challenge

#writing a function for bubblesort algo
def bubblesort(list):
    countSwap = 0 #initialize number of swaps as 0
    flagged = True
    while(flagged):
        for i in range(0, len(list)): #iterate through all the numbers in the list
            flagged = False
            #iterate through all the numbers in the list - 1, due to +1 index
            for j in range(0, len(list) - 1):
                #conditional statement to determine if need to swap
                if (list[j] > list[j+1]):
                    countSwap += 1 #increment countSwap by 1
                    temp = list[j] #swapping -
                    list[j] = list[j+1]
                    list[j+1] = temp
                    flagged = True
    #print(str(countSwap) + ' steps') #toggle comment for avg sorting time purposes
    return list #return the sorted list

#writing a function for combsort algo
def combsort(list):
    #initialize gap as length of list at first, and then rescale it using the gap
    gap = len(list)
    #initialize flagged is true to recalibrate gap before the first swap
    flagged = True
    countSwap = 0 #initialize countSwap as 0 as there are 0 swaps in the start
    while (flagged): #if flagged is true, then we must recalibrate gap
         #scaling factor is 1.3, so we must divide by 1.3
        newGap = int(gap/1.3)
        gap = max(1, newGap) #minimum gap has to be 1
        flagged = False #set flagged to false in the case there is no more swaps
        for i in range (0, len(list) - gap):
            #conditional statement to determine if need to swap
            if (list[i] > list[i + gap]):
                countSwap += 1 #increment countSwap by 1
                temp = list[i] #swapping -
                list[i] = list[i + gap]
                list[i + gap] = temp
                flagged = True #in order to recalibrate gap for the next swap
    #print(str(countSwap) + ' steps') #toggle comment for avg sorting time purposes
    return list #return the sorted list

#writing function to generate 1000 lists of 10 integers in randomized order
def generateLists(numberOfLists, numberOfInts):
    lists = [] #initialize an array
    #iterates through numberOfLists - 1 (runs 1000 times)
    for i in range(0, numberOfLists):
        #use random.sample() for rand arrays of 10 integers
        newList = random.sample(range(-1000, 1000), numberOfInts)
        lists.append(newList) #append the newList to the list (2D array)
    return lists #return the list with 1000 arrays of 10 integers in random order

#function to accomplish avg sort time for the two algorithms
def speedTest(): #remember to comment out print statements before running!
    testCase1 = generateLists(1000, 10) #generate 2D array containing 1000 randomized lists
    testCase1Copy =  copy.deepcopy(testCase1) #deepcopy the array for the other algorithm

    #speedtest for bubblesort
    startTestB = time.perf_counter() #start timer
    for i in range(0, 1000): #iterate sorting through all 1000 lists
        bubblesort(testCase1[i]) #bubblesort
    endTestB = time.perf_counter() #end timer
    timeB = endTestB - startTestB #total time elapsed
    avgTimeB = timeB/1000 #average time for sorting

    #speedtest for combsort
    startTestC = time.perf_counter() #start timer
    for j in range(0, 1000): #iterate sorting through all 1000 lists
        combsort(testCase1Copy[j]) #combsort
    endTestC = time.perf_counter() #end timer
    timeC = endTestC - startTestC #total time elapsed
    avgTimeC = timeC/1000 #average time for sorting

    #print results
    print('Bubblesort avg time: ' + str(avgTimeB) + 's')
    print('Combsort avg time: ' + str(avgTimeC) + 's')

#added a parameter factor to change scaling factor
def combsortFactor(list, factor):
    gap = len(list)
    flagged = True
    countSwap = 0
    while (flagged):
        newGap = int(gap/factor)
        gap = max(1, newGap)
        flagged = False
        for i in range (0, len(list) - gap):
            if (list[i] > list[i + gap]):
                countSwap += 1
                temp = list[i]
                list[i] = list[i + gap]
                list[i + gap] = temp
                flagged = True
    return list

#optimization test for scaling factor (narrowed to 1.298 ~ 1.302)
def optimizationTest():
    testCase2 = generateLists(200000, 100)
    testCase2Copy1 = copy.deepcopy(testCase2)
    testCase2Copy2 = copy.deepcopy(testCase2)
    testCase2Copy2 = copy.deepcopy(testCase2)
    testCase2Copy3 = copy.deepcopy(testCase2)
    testCase2Copy4 = copy.deepcopy(testCase2)
    startTestC = time.perf_counter() #start timer
    for a in range(0, 200000): #iterate sorting through all 1000 lists
        combsortFactor(testCase2[a], 1.298) #combsort
    endTestC = time.perf_counter() #end timer
    timeC = endTestC - startTestC #total time elapsed
    avgTimeC = timeC/200000
    print(avgTimeC)
    startTestC = time.perf_counter() #start timer
    for a in range(0, 200000): #iterate sorting through all 1000 lists
        combsortFactor(testCase2Copy1[a], 1.299) #combsort
    endTestC = time.perf_counter() #end timer
    timeC = endTestC - startTestC #total time elapsed
    avgTimeC = timeC/200000
    print(avgTimeC)
    startTestC = time.perf_counter() #start timer
    for a in range(0, 200000): #iterate sorting through all 1000 lists
        combsortFactor(testCase2Copy2[a], 1.300) #combsort
    endTestC = time.perf_counter() #end timer
    timeC = endTestC - startTestC #total time elapsed
    avgTimeC = timeC/200000
    print(avgTimeC)
    startTestC = time.perf_counter() #start timer
    for a in range(0, 200000): #iterate sorting through all 1000 lists
        combsortFactor(testCase2Copy3[a], 1.301) #combsort
    endTestC = time.perf_counter() #end timer
    timeC = endTestC - startTestC #total time elapsed
    avgTimeC = timeC/200000
    print(avgTimeC)
    startTestC = time.perf_counter() #start timer
    for a in range(0, 200000): #iterate sorting through all 1000 lists
        combsortFactor(testCase2Copy4[a], 1.302) #combsort
    endTestC = time.perf_counter() #end timer
    timeC = endTestC - startTestC #total time elapsed
    avgTimeC = timeC/200000
    print(avgTimeC)

#testing sample case with bubblesort
list1 = [5, 0, 9, 8, 7, 1, 4, 3, 2, 6]
print('Bubblesort')
print(list1)
print(bubblesort(list1)) #26 steps; [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#testing sample case with combsort
list2 = [5, 0, 9, 8, 7, 1, 4, 3, 2, 6]
print('Combsort')
print(list2)
print(combsort(list2)) #10 steps; [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print('------------------------------')
#testing challenge problem
print('Challenge') #make sure to comment out print statements!!!
speedTest(); #run the function for testing speed of algorithms
#Bubblesort avg time: 1.1210799999999744e-05s
#Combsort avg time: 5.633200000000116e-06s
'''Results vary every time the function is run due to uniquely generated 1000
lists of 10 integers in an array.'''
#testing the scaling factors
optimizationTest(); #optimize the scaling factors
