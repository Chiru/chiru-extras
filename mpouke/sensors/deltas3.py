import csv
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = csv.reader(open('3dgestures.csv'), delimiter=',')
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

time = float(0.1)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def velocity(ini, acc, time):
	vel = ini + acc*time
	return vel

#for row in data:
#	for range in 150:
#		gestures.append(row[:3])
	

for row in data:
	counter = 0
	xs = []
	ys = []
	zs = []
	while counter < 150:
	
		accx = float(row[0])
		accy = float(row[1])
		accz = float(row[2])

		velx = velocity(initialx, accx, time)
		vely = velocity(initialy, accy, time)
		velz = velocity(initialz, accz, time)
		 
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

		counter = counter + 1
		
		row = data.next()

	ax.scatter(xs, ys, zs, s=20, c='b')
	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')

	print xs
	plt.show()
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