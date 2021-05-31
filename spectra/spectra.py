import numpy as np
import matplotlib.pyplot as plt

pixel, counts = np.loadtxt('alpheratz.csv', unpack=True, delimiter=',')

x = np.array([725.5, 525])
y = np.array([435.8, 546.1])
