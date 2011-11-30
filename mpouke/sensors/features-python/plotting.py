import extract as ex
import pylab
import numpy
#you can also use from extract import *
#yet this makes it hard to reload the module, if changed

dfname = './assemblynew.dat';
#dfname = './testdata.dat';


#load the motion sensor data into the respective variables
#data = pylab.load(dfname);
data = numpy.loadtxt(dfname);

#plot the accelerometer data from the wrist
pylab.plot(data[:,2:5])
pylab.show()

#do a sliding window analysis over the x axis of the accelerometer
#you can also add functions on your own
#herer median and variance will be extracted
idx= (data[:,11]== 1).nonzero()
hammering=data[idx, 2:5][0]
idx= (data[:,11]== 3).nonzero()
sandpapering=data[idx, 2:5][0]

pylab.figure()
pylab.plot(hammering)
pylab.show()
fs = [numpy.median,numpy.var];
hammerFeat =ex.extract(hammering[:,1], 50, 0, fs);
sandFeat =ex.extract(sandpapering[:,1],50, 0, fs);

#to generate a scatter plot use:
pylab.figure()
pylab.plot(hammerFeat[:,0], hammerFeat[:,1],'r+',sandFeat[:,0], sandFeat[:,1],'b+');
pylab.show()

