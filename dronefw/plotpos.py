import matplotlib.pyplot as plt
import numpy as np
import csv

#plt.ion()

#fig, ax = plt.subplots()

#plot = ax.scatter([], [])
#ax.set_xlim(-5, 5)
#ax.set_ylim(-5, 5)


data = np.genfromtxt('posfile', dtype=float,delimiter=',')


xdata=data[:,0]
ydata=data[:,1]

plot=plt.scatter(xdata,ydata)
plt.show()

