#!/usr/bin/env python
"""
Example: simple line plot.
Show how to make and save a simple line plot with labels, title and grid
"""
import numpy
import pylab
import csv

rowcount=0
t=[]
ax=[]
ay=[]
az=[]
gx=[]
gy=[]
gz=[]

with open('completegestures.csv') as file:

	csvReader = csv.reader((file), delimiter=',')
	for row in csvReader:
		rowcount=rowcount+1	
		if rowcount > 13:
			t.append(row[0])
			ax.append(row[1])
			ay.append(row[2])
			#az.append(row[3])
			#gx.append(row[4])
			#gy.append(row[5])
			#gz.append(row[6])
	#t = numpy.arange(0.0, 1.0+0.01, 0.01)
	#s = numpy.cos(2*2*numpy.pi*t)
	a=numpy.asarray(ax)
	e=sum(numpy.abs(a)**2)
	pylab.plot(e)

	pylab.xlabel('time (milliseconds)')
	pylab.ylabel('Acceleration x axis')
	pylab.title('Accelerometer data test')
	pylab.grid(True)
	pylab.savefig('simple_plot')

	pylab.show()

