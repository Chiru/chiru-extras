import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from numpy import linalg as LA
from scipy import integrate

data = csv.reader(open('demo.csv'), delimiter=',')
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
        coordinates=np.array([])
	gestureacc=np.array([])
	allaccx=np.array([])
	allaccy=np.array([])
	allaccz=np.array([])
	turnedx=np.array([])
	turnedy=np.array([])
	turnedz=np.array([])

	fftvelx=np.zeros(shape=(256,1))
	fftvely=np.zeros(shape=(256,1))
	fftvelz=np.zeros(shape=(256,1))


	initialx = float(0)
	initialy = float(0)
	initialz = float(0)

	initialposx = float(0)
	initialposy = float(0)
	initialposz = float(0)
	while counter < 256:
	
                #if abs(float(row[0])) < 15: accx=float(0)
		#else: accx = float(row[0])
                accx = float(row[0])
		#accy = float(row[1]-1000)
                #if abs(float(row[1])) < 15: accy=float(0)
		#else: accy = float(row[1])
		#accy = accy - 1000
                accy = float(row[1])
		accz = float(row[2])

		allaccx = np.append(allaccx,accx)
		allaccy = np.append(allaccy,accy)
		allaccz = np.append(allaccz,accz)
		#print allaccx
		
		counter = counter + 1
		
		row = data.next()

	meanx = allaccx.mean()	
	meany = allaccy.mean()
	meanz = allaccz.mean()

	meanvector = np.array([meanx, meany, meanz])

        xymatrix = np.array([[1,0,0],[0,1,0],[0,0,0]])

	xyprojection = np.dot(meanvector,xymatrix)
        xaxis = np.array([1,0,0])
	alpha = np.arccos(np.dot(xyprojection,xaxis)/(LA.norm(xyprojection)*LA.norm(xaxis)))
        beta = np.arccos(np.dot(meanvector,xyprojection)/(LA.norm(meanvector)*LA.norm(xyprojection)))


	#xyprojection = list(meanvector)
	#xyprojection[2]=0
	#meanmagn = LA.norm(meanvector)
	#projmagn = LA.norm(xyprojection)
	#unitmean = meanvector/meanmagn
	#unitproj = xyprojection/projmagn	
	#xaxis = np.array([1,0,0])	

	#print meanmagn
	#print projmagn	
	
	#xynormal = np.array([0,0,1])
	#xyangle = np.arccos(np.dot(unitmean,xynormal))
	#print xyangle
	#xyangle = np.degrees(xyangle)	
	#print xyangle

	#products = np.dot(unitmean,xaxis)
	 
	#print products

	#alpha = np.arccos(products)
	#alpha = np.degrees(alpha)
	#beta = 90-xyangle
	#print beta
	#beta = np.radians(beta)
	#print beta
	#print alpha
	#print beta

	mrot = np.array([[((np.cos(alpha))**2)*np.sin(beta)+(np.sin(alpha))**2,(np.cos(alpha))*np.sin(alpha)*(np.sin(beta)-1),-(np.cos(alpha))*np.cos(beta)],
		           [np.cos(alpha)*np.sin(alpha)*(np.sin(beta)-1),((np.sin(alpha))**2)*np.sin(beta)+(np.cos(alpha))**2,-(np.sin(alpha))*np.cos(beta)],
	                   [np.cos(alpha)*np.cos(beta),np.sin(alpha)*np.cos(beta),np.sin(beta)]])

	
	for i,j,k in zip(allaccx,allaccy,allaccz):
		accsample = [i,j,k]
		#print accsample
		turned = np.dot(accsample,mrot)
		#print turned
                #turned=np.array(accsample)

		acx = turned[0]
		acy = turned[1]
		acz = turned[2]
		
		turnedx = np.append(turnedx,acx)	
		turnedy = np.append(turnedy,acy)
		turnedz = np.append(turnedz,acz)	
			
	turnedx = (turnedx-np.mean(turnedx))/np.std(turnedx)
	turnedy = (turnedy-np.mean(turnedy))/np.std(turnedy)
	turnedz = (turnedz-np.mean(turnedz))/np.std(turnedz)

	#allaccx = (allaccx-np.mean(allaccx))/np.std(allaccx)
	#allaccy = (allaccy-np.mean(allaccy))/np.std(allaccy)
	#allaccz = (allaccz-np.mean(allaccz))/np.std(allaccz)	
	

	#turnedx = (turnedx-np.mean(turnedx))
	#turnedy = (turnedy-np.mean(turnedy))
	#turnedz = (turnedz-np.mean(turnedz))	



	#freqx = np.fft.fft(turnedx,256)
	#freqy = np.fft.fft(turnedy,256)
	#freqz = np.fft.fft(turnedz,256)


	#freqx[:2]=0
	#freqy[:2]=0
	#freqz[:2]=0	

	#invx = np.fft.ifft(freqx)
	#invy = np.fft.ifft(freqy)
	#invz = np.fft.ifft(freqz)

	#tx = invx.real
	#ty = invy.real
	#tz = invz.real
	
        velx = integrate.cumtrapz(turnedx,x=None,dx=0.01,axis=-1)
        vely = integrate.cumtrapz(turnedy,x=None,dx=0.01,axis=-1)
	velz = integrate.cumtrapz(turnedz,x=None,dx=0.01,axis=-1)       

        xs = integrate.cumtrapz(velx,x=None,dx=0.01,axis=-1)
        ys = integrate.cumtrapz(vely,x=None,dx=0.01,axis=-1)
        zs = integrate.cumtrapz(velz,x=None,dx=0.01,axis=-1)

	#print turnedx

        p0 = np.array([xs[0],ys[0],zs[0]])
        #print p0
        centroid = np.array([np.mean(xs),np.mean(ys),np.mean(zs)])
        #print centroid

        theta = np.arccos(np.dot(p0,centroid)/(LA.norm(p0)*LA.norm(centroid)))
        theta = theta*-1

        n = np.cross(p0,centroid)/LA.norm(np.cross(p0,centroid))
        nx = np.array(n[0])
        ny = np.array(n[1])
        nz = np.array(n[2])

        #print theta
        #print nx
        #print ny
        #print nz

        irot = np.array([[(nx**2)*(1-np.cos(theta))+np.cos(theta),nx*ny*(1-np.cos(theta))+nz*np.sin(theta),nx*nz*(1-np.cos(theta))-ny*np.sin(theta)],
                         [nx*ny*(1-np.cos(theta))-nz*np.sin(theta),(ny**2)*(1-np.cos(theta))+np.cos(theta),ny*nz*(1-np.cos(theta))+nx*np.sin(theta)],
                         [nx*nz*(1-cos(theta))+ny*sin(theta),ny*nz*(1-np.cos(theta))-nx*np.sin(theta),(nz**2)*(1-np.cos(theta))+np.cos(theta)]])

        
        gx=np.array([])
        gy=np.array([])
        gz=np.array([])

        for a,b,c in zip(xs,ys,zs):
            v=np.array([a,b,c])
            #print 'before: ',v
            vt=np.dot(v,irot)
            #print 'after: ',vt
            
            gx=np.append(gx,vt[0])
            gy=np.append(gy,vt[1])
            gz=np.append(gz,vt[2])

        #print gx
        #print gy
        #print gz

	#print turnedx
	#print turnedy
	#print turnedz

	#for a,b,c in zip(tx,ty,tz):
		
		#print c

		#velx = velocity(initialx, a, time)
		#vely = velocity(initialy, b, time)
		#velz = velocity(initialz, c, time)
		

 
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

	#print positions
        #print len(positions)

	ax.scatter(gx, gy, gz, s=20, c='b')
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
