import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from numpy import linalg as LA

data = csv.reader(open('final.csv'), delimiter=',')
xs = []
ys = []
zs = []
positions = np.array([])
gestureTx = np.array([])
gestureTy = np.array([])
gestureTz = np.array([])
alldeltasx = np.array([])
alldeltasy = np.array([])
alldeltasz = np.array([])
previousx = float(0)
previousy = float(0)
previousz = float(0)

initialposx = float(0)
initialposy = float(0)
initialposz = float(0)

time = float(0.01)

ion()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for row in data:
    accelerations=np.array([])
    accx=np.array([])
    accy=np.array([])
    accz=np.array([])
    deltasx=np.array([])
    deltasy=np.array([])
    deltasz=np.array([])
    counter = 0
    while counter < 256:
        if counter==0:
            previousx=float(row[0])
            previousy=float(row[1])
            previousz=float(row[2])
        currentx=float(row[0])
        currenty=float(row[1])
        currentz=float(row[2])
        #print 'prev: ',previousx
        #print 'curr: ',currentx
        accx = np.append(accx,currentx)
        accy = np.append(accy,currenty)
        accz = np.append(accz,currentz)
        accelerations = np.append(accelerations,[currentx,currenty,currentz])
        deltax=previousx-currentx
        deltay=previousy-currenty
        deltaz=previousz-currentz
        #print deltax
        deltasx = np.append(deltasx,deltax)
        deltasy = np.append(deltasy,deltay)
        deltasz = np.append(deltasz,deltaz)
        previousx=currentx
        previousy=currenty
        previousz=currentz           
        counter=counter+1
        row=data.next()
    alldeltasx = np.append(alldeltasx,deltasx)
    alldeltasy = np.append(alldeltasy,deltasy)
    alldeltasz = np.append(alldeltasz,deltasz)

    xs = np.array([])
    ys = np.array([])
    zs = np.array([])
    x = 0
    y = 0
    z = 0
    for a,b,c in zip(deltasx,deltasy,deltasz):
        x += a
        y += b    
        z += c
        xs = np.append(xs,x)
        ys = np.append(ys,y)
        zs = np.append(zs,z)
    #print xs

    ax.scatter(xs, ys, zs, s=20, c='b')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    draw()
    raw_input("Press enter when done...")