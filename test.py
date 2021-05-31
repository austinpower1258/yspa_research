import operator as op
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2

def func():
    count = 0
    for i in range(0, 1001):
        if ((i**3 + 12 * i**2 - i - 12) % 1001 == 0):
            count += 1
    return count

def func1():
    count = 0
    for i in range(0, 2021):
        if (ncr(2020, i) % 3 != 0):
            count += 1
    return count

def func2():
    for x in range(1, 1001):
        for y in range(1, 1001):
            for n in range(1, 11):
                if(x**2 - 5*y**2 == 5**(2*n)):
                    print('x: ' + str(x))
                    print('y: ' + str(y))



print(func())
print(func1())
print(func2())
