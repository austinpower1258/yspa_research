import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

days, absmags = np.loadtxt('IIL.txt', unpack =True, skiprows = 1)
jdn, myapp_g, myapp_r = np.loadtxt("csv.csv", unpack = True, skiprows =1, delimiter = ',')
myday = [i-jdn[0] for i in jdn]

model = interp1d(days, absmags, kind="cubic")
x = np.linspace(min(days),max(days),num=500)
y = model(x)
print(min(y))

def get(myapp,myday):
    dmod = 35.5
    myabs = myapp - dmod
    res = model(myday) - myabs
    rms = np.sqrt(np.sum(res**2)/len(myday))
    changerms = 1.
    changemod = 0.5

    while abs(changerms) > 10**(-64):
        oldrms = rms
        dmod += changemod
        myabs = myapp - dmod
        res = model(myday) - myabs
        rms = np.sqrt(np.sum(res**2)/len(myday))
        changerms = oldrms - rms
        if changerms < 0:
            changemod *= -0.5
    return dmod,rms,myabs

def graph(myapp,myday):
    myabs = get(myapp,myday)[2]
    delta = myabs[0] - myapp[0] + 33.25


    plt.errorbar([i - 1.83 for i in myday], myabs, xerr = 0.05, yerr = get(myapp, myday)[1],fmt='o')
    line, = plt.plot([i-1.83 for i in x], y, color ='blue')


    plt.xlim(-5, 40)
    plt.ylim(max(absmags)-0.5, min(y-delta)-0.5)
    plt.xlabel('Days since peak')
    plt.ylabel('Absolute magnitude')
    plt.title("Sloan g Light Curve & Type II-L Model")
    plt.show()

def minday(myapp1, myapp2, myday):
    for i in np.linspace(-5, 10, num=100):
        a = get(myapp1, myday)[1]
        b = get(myapp2, myday)[1]
        c = get(myapp1,[k+i for k in myday])[1]
        d = get(myapp2,[k+i for k in myday])[1]
        if  a+b > c+d :
            myday = [k+i for k in myday]
    return myday

newday = minday(myapp_r, myapp_g, myday)
print(get(myapp_g,newday)[:2])
graph(myapp_g,newday)
print(get(myapp_r,newday)[:2])
graph(myapp_r,newday)
print(float(newday[0]) - float(myday[0]))
