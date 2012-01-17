import csv
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from numpy import linalg as LA

data = csv.reader(open('3dgestures3.csv'), delimiter=',')
xs = []
ys = []
zs = []
positions = []
gestures = [] 
initialx = float(0)
initialy = float(0)
initialz = float(0)

initialposx = float(0)
initialposy = float(0)
initialposz = float(0)

ion()

time = float(0.1)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def velocity(ini, acc, time):
	vel = ini + acc*time
	return vel

#def magnitude(a)
#	for 

#for row in data:
#	for range in 150:
#		gestures.append(row[:3])
	
fign = 0
for row in data:
	fign = int(fign) + 1
	counter = 0
	xs = []
	ys = []
	zs = []
	gestureacc=numpy.array([])
	allaccx=numpy.array([])
	allaccy=numpy.array([])
	allaccz=numpy.array([])
	turnedx=numpy.array([])
	turnedy=numpy.array([])
	turnedz=numpy.array([])


	initialx = float(0)
	initialy = float(0)
	initialz = float(0)

	initialposx = float(0)
	initialposy = float(0)
	initialposz = float(0)
	while counter < 150:
	
		accx = float(row[0])
		#accy = float(row[1]-1000)
		accy = float(row[1])
		#accy = accy - 1000
		accz = float(row[2])

		allaccx = numpy.append(allaccx,accx)
		allaccy = numpy.append(allaccy,accy)
		allaccz = numpy.append(allaccz,accz)
		#print allaccx
		
		counter = counter + 1
		
		row = data.next()
	
	#gestureacc = numpy.append(gestureacc,allaccx,axis=1)	
	#gestureacc = numpy.append(gestureacc,allaccy,axis=1)
	#gestureacc = numpy.append(gestureacc,allaccz,axis=1)

	#print gestureacc

	meanx = allaccx.mean()	
	meany = allaccy.mean()
	meanz = allaccz.mean()

	meanvector = [meanx, meany, meanz]
	xyprojection = list(meanvector)
	xyprojection[2]=0
	meanmagn = LA.norm(meanvector)
	projmagn = LA.norm(xyprojection)
	unitmean = meanvector/meanmagn
	unitproj = xyprojection/projmagn	
	xaxis = numpy.array([1,0,0])	

	#print meanmagn
	#print projmagn	
	
	xynormal = numpy.array([0,0,1])
	xyangle = numpy.arccos(numpy.dot(unitmean,xynormal))
	print xyangle	

	products = numpy.dot(unitmean,xaxis)
	 
	#print products

	alpha = numpy.arccos(products)
	print alpha
	beta = 90-xyangle
	print beta
	#print alpha
	#print beta

	mrot = numpy.array([[(((numpy.cos(alpha))**2)*numpy.sin(beta)+(numpy.sin(alpha))**2),((numpy.cos(alpha))*numpy.sin(alpha)*(numpy.sin(beta-1))),-(numpy.cos(alpha))*numpy.cos(beta)],
		           [(numpy.cos(alpha)*numpy.sin(alpha)*(numpy.sin(beta-1))),(((numpy.sin(alpha))**2)*numpy.sin(beta)+(numpy.cos(alpha))**2),-(numpy.sin(alpha))*numpy.cos(beta)],
	                   [(numpy.cos(alpha)*numpy.cos(beta)),(numpy.sin(alpha)*numpy.cos(beta)),(numpy.sin(beta))]])

	
	for i,j,k in zip(allaccx,allaccy,allaccz):
		accsample = [i,j,k]
		#print accsample
		turned = numpy.dot(accsample,mrot)
		#print turned

		acx = turned[0]
		acy = turned[1]
		acz = turned[2]
		
		turnedx = numpy.append(turnedx,acx)	
		turnedy = numpy.append(turnedy,acy)
		turnedz = numpy.append(turnedz,acz)	
			
	#turnedx /= numpy.max(numpy.abs(turnedx))
	#turnedy /= numpy.max(numpy.abs(turnedy))
	#turnedz /= numpy.max(numpy.abs(turnedz))

	turnedx = (turnedx-numpy.mean(turnedx))/numpy.std(turnedx)
	turnedy = (turnedy-numpy.mean(turnedy))/numpy.std(turnedy)
	turnedz = (turnedz-numpy.mean(turnedz))/numpy.std(turnedz)

	print int(numpy.mean(turnedz))
	print numpy.var(turnedz)

	#print turnedx
	#print turnedy
	#print turnedz


	for a,b,c in zip(turnedx,turnedy,turnedz):
		
		#print c

		velx = velocity(initialx, a, time)
		vely = velocity(initialy, b, time)
		velz = velocity(initialz, c, time)
		 
		posx = initialposx + velx*time
		posy = initialposy + vely*time
		posz = initialposz + velz*time

		positions.append([posx,posy,posz])
		xs.append(posx)
		ys.append(posy)
		zs.append(posz)

		initialx = velx
		initialy = vely
		initialz = velz
	
		initialposx = posx
		initialposy = posy
		initialposz = posz		

	#print meanvector

	ax.scatter(xs, ys, zs, s=20, c='b')
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')

	#print xs
	draw()
	raw_input("Press enter when done...")
	#fign = str(fign)
	#plt.savefig(fign+'.png')
	#print xs
	#row = data.next()

	#ax.scatter(posx,posy,posz, s=20, c='b')


#print positions

	#xlist.append(row[0])
	#ylist.append(row[1])
	#zlist.append(row[2])



#for x in xlist:
#	acc = float(x)
#	final = velocity(initial, acc, float(0.1))
#	initial = final
#	print initial

#new_position = current_position + velocity * elapsed
