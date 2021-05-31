import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

days, absmags = np.loadtxt('Ia.txt', unpack =True, skiprows = 1)

myday = np.array([0,7,8.1,11.04,15,18.1,25])
myapp_g = np.array([16.60,16.80,16.91,17.07,17.11,17.26,17.69])
myapp_r = np.array([16.61, 16.72, 16.94, 17.06, 17.14, 17.21, 17.60])

model = interp1d(days, absmags, kind="cubic")
x = np.linspace(min(days),max(days),num=500)
y = model(x)

def find(myapp,myday):
    dmod = 35.5
    myabs = myapp - dmod
    res = model(myday) - myabs
    rms = np.sqrt(np.sum(res**2))
    changerms = 1.0
    changemod = 0.5

    while abs(changerms) > 1e-64:
        oldrms = rms
        dmod += changemod
        myabs = myapp - dmod
        res = model(myday) - myabs
        rms = np.sqrt(np.sum(res**2))
        changerms = oldrms - rms
        if changerms < 0:
            changemod *= -0.5
    return dmod,rms,myabs

def graph(myapp,myday):
    myabs = find(myapp,myday)[2]
    plt.scatter(myday, myabs)
    plt.plot(x,y, color ='blue')
    plt.ylim(max(absmags), min(absmags))
    plt.show()

def minday(myapp1, myapp2, myday):
    for i in np.linspace(0,20,num=100):
        a = find(myapp1, myday)[1]
        b = find(myapp2, myday)[1]
        c = find(myapp1,[k+i for k in myday])[1]
        d = find(myapp2,[k+i for k in myday])[1]
        if  a+b > c+d :
            myday = [k+i for k in myday]
    return myday

newday = minday(myapp_r, myapp_g, myday)
print(find(myapp_g,newday)[:2])
graph(myapp_g,newday)
print(find(myapp_r,newday)[:2])
graph(myapp_r,newday)
print(newday[0] - myday[0])
