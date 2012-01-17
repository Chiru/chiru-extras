import csv
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from numpy import linalg as LA

data = csv.reader(open('3dgesturesfft2.csv'), delimiter=',')
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

time = float(0.01)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

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

	fftvelx=numpy.zeros(shape=(256,1))
	fftvely=numpy.zeros(shape=(256,1))
	fftvelz=numpy.zeros(shape=(256,1))


	initialx = float(0)
	initialy = float(0)
	initialz = float(0)

	initialposx = float(0)
	initialposy = float(0)
	initialposz = float(0)
	while counter < 256:
	
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

	#print numpy.fft.ifft(numpy.fft.fft(allaccx))

	freqx = numpy.fft.fft(allaccx,256)
	freqy = numpy.fft.fft(allaccy,256)
	freqz = numpy.fft.fft(allaccz,256)

	#print len(freqx)

	#print freqx
	#print numpy.fft.ifft(freqx)

	#print freqx
	
	counter=0	

	for i in freqx:
		omega = 2*numpy.pi*i
		#print omega
		displacement = -(omega**2)
		#print abs(displacement)
		#numpy.append(fftvelx,displacement)
		freqx[counter]=displacement
		counter=counter+1		
			
	counter=0

	for i in freqy:
		omega = 2*numpy.pi*i
		displacement = -(omega**2)
		freqy[counter]=displacement
		counter=counter+1

	counter=0

	for i in freqz:
		omega = 2*numpy.pi*i
		displacement = -(omega**2)
		#numpy.append(fftvelz,displacement)
		freqz[counter]=displacement
		counter=counter+1

	#print freqx

	turnedx = numpy.fft.ifft(freqx)
	turnedy = numpy.fft.ifft(freqy)
	turnedz = numpy.fft.ifft(freqz)

	xs = turnedx.real
	ys = turnedy.real
	zs = turnedz.real
	
	#print turnedx


	#print turnedx
	#print turnedy
	#print turnedz

	#for a,b,c in zip(turnedx,turnedy,turnedz):
		
		#print c

	#	velx = velocity(initialx, a, time)
	#	vely = velocity(initialy, b, time)
	#	velz = velocity(initialz, c, time)
		 
	#	posx = initialposx + velx*time
	#	posy = initialposy + vely*time
	#	posz = initialposz + velz*time

	#	positions.append([posx,posy,posz])
	#	xs.append(posx)
	#	ys.append(posy)
	#	zs.append(posz)

	#	initialx = velx
	#	initialy = vely
	#	initialz = velz
	
	#	initialposx = posx
	#	initialposy = posy
	#	initialposz = posz		

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
