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

def velocity(ini, acc, time):
	vel = ini + acc*time
	return vel

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
	#print xyangle
	xyangle = numpy.degrees(xyangle)	
	#print xyangle

	products = numpy.dot(unitmean,xaxis)
	 
	#print products

	alpha = numpy.arccos(products)
	#alpha = numpy.degrees(alpha)
	beta = 90-xyangle
	#print beta
	beta = numpy.radians(beta)
	#print beta
	#print alpha
	#print beta

	mrot = numpy.array([[((numpy.cos(alpha))**2)*numpy.sin(beta)+(numpy.sin(alpha))**2,(numpy.cos(alpha))*numpy.sin(alpha)*(numpy.sin(beta)-1),-(numpy.cos(alpha))*numpy.cos(beta)],
		           [numpy.cos(alpha)*numpy.sin(alpha)*(numpy.sin(beta)-1),((numpy.sin(alpha))**2)*numpy.sin(beta)+(numpy.cos(alpha))**2,-(numpy.sin(alpha))*numpy.cos(beta)],
	                   [numpy.cos(alpha)*numpy.cos(beta),numpy.sin(alpha)*numpy.cos(beta),numpy.sin(beta)]])

	
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
			
	#turnedx = (turnedx-numpy.mean(turnedx))/numpy.std(turnedx)
	#turnedy = (turnedy-numpy.mean(turnedy))/numpy.std(turnedy)
	#turnedz = (turnedz-numpy.mean(turnedz))/numpy.std(turnedz)

	allaccx = (allaccx-numpy.mean(allaccx))/numpy.std(allaccx)
	allaccy = (allaccy-numpy.mean(allaccy))/numpy.std(allaccy)
	allaccz = (allaccz-numpy.mean(allaccz))/numpy.std(allaccz)	
	

	#turnedx = (turnedx-numpy.mean(turnedx))
	#turnedy = (turnedy-numpy.mean(turnedy))
	#turnedz = (turnedz-numpy.mean(turnedz))	



	#freqx = numpy.fft.fft(turnedx,256)
	#freqy = numpy.fft.fft(turnedy,256)
	#freqz = numpy.fft.fft(turnedz,256)


	#freqx[:2]=0
	#freqy[:2]=0
	#freqz[:2]=0	

	#print freqx

	#print len(freqx)

	#print freqx
	#print numpy.fft.ifft(freqx)

	#print freqx
	
	#counter=0	

	#for i in freqx:
	#	if counter < 3:
	#		displacement=0
	#	else:
	#		f=100
	#		omega = 2*numpy.pi*f
	#		k=(2*numpy.pi)/omega
			#print omega
	#		displacement = i/(-(omega**2))
			#print abs(displacement)
			#numpy.append(fftvelx,displacement)

	#		freqx[counter]=displacement
	#	counter=counter+1		
			
	#counter=0

	#for i in freqy:
	#	if counter < 3:
	#		displacement=0
	#	else:
	#		f=100
	#		omega = 2*numpy.pi*f
	#		displacement = i/(-(omega**2))
	#		freqy[counter]=displacement
	#	counter=counter+1

	#counter=0

	#for i in freqz:
	#	if counter < 3:
	#		displacement=0
	#	else:
	#		f=100
	#		omega = 2*numpy.pi*f
	#		displacement = i/(-(omega**2))
			#numpy.append(fftvelz,displacement)
	#		freqz[counter]=displacement
	#	counter=counter+1

	#print freqx

	#invx = numpy.fft.ifft(freqx)
	#invy = numpy.fft.ifft(freqy)
	#invz = numpy.fft.ifft(freqz)

	#tx = invx.real
	#ty = invy.real
	#tz = invz.real
	
	#print turnedx


	#print turnedx
	#print turnedy
	#print turnedz

	for a,b,c in zip(allaccx,allaccy,allaccz):
		
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