# Austin Wang, July 1, 2020
#With this code, I hope to write a function that will approximate the value of
#the base of the natural log, e, the Gaussian constant, the best number

import math

# This is a comment...
# Taylor series for e**1 = 1 + 1 + 1/2! + 1/3! + ...

def nat(N):
    total = 0.0
    for i in range(N):
        total += 1**i/math.factorial(i)
    return total

def recursive_factorial(num):
    if (num == 1): #base case; so when num == 1 => 1! = 1
        return 1
    else:
        return num * recursive_factorial(num-1) #recursive function

def my_for_loop_factorial(num):
    product = 1
    for i in range(1, num + 1):
        product *= i
    return product

print(recursive_factorial(13)) #returns 6227020800
print(my_for_loop_factorial(13)) #returns 6227020800
