import math

def genList(n):
    list = []
    for i in range(0, n):
        list[i] = i
    return list

def func1():
    for n in range(1, 2022):
        genList(n)
