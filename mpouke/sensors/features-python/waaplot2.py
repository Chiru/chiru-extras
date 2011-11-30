#!/usr/bin/env python
"""
Example: simple line plot.
Show how to make and save a simple line plot with labels, title and grid
"""
import numpy
import pylab
import csv
import extract as ex

rowcount=0
t=[]
ax=[]
ay=[]
az=[]
gx=[]
gy=[]
gz=[]

#fs=[numpy.median,numpy.std]
fs=[numpy.mean]

with open('testdata2.dat') as file:

	csvReader = csv.reader((file), delimiter=',')
	for row in csvReader:
		rowcount=rowcount+1	
		if rowcount > 13:
			print row
			t.append(row[0])
			ax.append(row[1])
			ay.append(row[2])
			az.append(row[3])
			gx.append(row[4])
			gy.append(row[5])
			gz.append(row[6])
	#t = numpy.arange(0.0, 1.0+0.01, 0.01)
	#s = numpy.cos(2*2*numpy.pi*t)
	data = numpy.loadtxt(ax);
	data2 = numpy.loadtxt(ay);
	data3 = numpy.loadtxt(az);
	axfeat = ex.extract(data,2,0,fs)
	yxfeat = ex.extract(data2,2,0,fs)	
	azfeat = ex.extract(data3,2,0,fs)

	pylab.plot(t,ax)
	pylab.plot(t,ay)
	pylab.plot(t,az)
	pylab.plot(t,gx)
	pylab.plot(t,gy)
	pylab.plot(t,gz)
	#pylab.plot(axfeat)
	#pylab.plot(yxfeat)
	#pylab.plot(azfeat)	

	pylab.xlabel('time (milliseconds)')
	pylab.ylabel('Acceleration x axis')
	pylab.title('Accelerometer data test')
	pylab.grid(True)
	pylab.savefig('simple_plot')

	pylab.show()

