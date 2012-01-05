import csv
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from numpy import linalg as LA

data = csv.reader(open('3dgestures2.csv'), delimiter=',')
xs = []
ys = []
zs = []
positions = [[0,0,0]]
gestures = []
deltas = [] 


initialposx = float(0)
initialposy = float(0)
initialposz = float(0)

for row in data:
	initialx = float(0)
	initialy = float(0)
	initialz = float(0)
	counter = 0
	while counter < 150
		deltax = float(row[0])-initialx
		deltay = float(row[1])-initialy
		deltaz = float(row[2])-initialz
		deltas.append([deltax,deltay,deltaz])
		row = data.next()
	
	print deltas
