import math

product = 1
for x in range(-1000, 1000):
    for y in range(-1000, 1000):
        if (3 * x**2 + 3 * x + 1641 == 9 * y**3):
            print(x)
            product *= abs(x)
print(product)
