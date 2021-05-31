# Austin Wang, June 30, 2020
#With this code, I hope to write a function that will convert temperatures
#from Celsius to Fahrenheit and Fahrenheit to Celsius. I will also calculate
#when the temperature values are equal in both units.

def convertCelsiusToFahrenheit(tempC):
  return (9/5) * tempC + 32

def convertFahrenheitToCelsius(tempF):
    return (5/9) * (tempF - 32)

def convertCelsiusToKelvin(tempC):
    return tempC + 273.15

def compareValues():
    for i in range(-100, 100):
        for j in range(-100, 100):
            if (convertCelsiusToFahrenheit(i) == (convertFahrenheitToCelsius(j))):
                print(i)

compareValues()
print(convertCelsiusToFahrenheit(21))
print(convertCelsiusToFahrenheit(4))
print(convertCelsiusToFahrenheit(12))
print(convertCelsiusToFahrenheit(23))
print(convertCelsiusToFahrenheit(28))
print(convertCelsiusToFahrenheit(32))

print(convertFahrenheitToCelsius(70))
print(convertFahrenheitToCelsius(80))
print(convertFahrenheitToCelsius(90))
print(convertFahrenheitToCelsius(100))
print(convertFahrenheitToCelsius(80))
print(convertFahrenheitToCelsius(70))
print(convertFahrenheitToCelsius(50))
