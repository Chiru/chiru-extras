import serial
from time import sleep
#import datetime
import csv
#import svmcomplete
import numpy
import pywt
#output = csv.writer(open('directions.csv', 'wb'), delimiter=',')

port = "/dev/rfcomm0"
ser = serial.Serial(port, baudrate=9600, timeout=10)
print "connecting..."
sleep(2)
ser.write("echo on"+"\r\n")      # write a string
#ser.write("echo on"+"\r\n")      # write a string
ser.write("hello"+"\r\n")
ser.write("sett 104900000"+"\r\n")
ser.write("ags +000005000 10 1 0"+"\r\n")
print ser.portstr 

#fs = [numpy.mean,numpy.std,numpy.fft.fft,]

#def extract(data, fs):
#    """Function calculates features over a data array in a slinding window
#    of size wsize with given overlap. The features calculated are
#    determined by a function list fs. 
#    """
#    total=data.size
#    features = zeros((total, len(fs)));
#    k = 0;
#    for func in fs:
#        for i in range (0, total):
#            features[i,k] = func(data)
#            i = i +wsize- overlap;
#        k = k + 1
#    return features

try:

	while True:
	    buffer = ser.read(ser.inWaiting())
	    feature=[]
	    for i in range(64):
		    vector=[]
		    #print "Got here"
		    data = ser.readline()
		    #print "Read line"
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 6:
			ax = vector[3]
			feature.append(float(ax))
			#print ax
			#line = vector[-6:]
			#iline = [float(n) for n in line]
			#print vector[-6:]
			#output.writerow(line)
		   	#result=svmcomplete.classify(iline)
			#print result
		    #sleep(0.5)
		    #print 'not blocked'
	    #print feature
	    npfeature = numpy.asarray(feature)
	    #print npfeature
	    b = abs(npfeature)
	    a = b**2
	    #e=sum(abs(feature)**2)
	    e = sum(a)
	    #print npfeature
	    print e
	    wp = pywt.WaveletPacket(data=feature, wavelet='db3', mode='sym')
	    aaa = wp['aaa'].data
	    print aaa
	    ff = numpy.fft.fft(aaa)
	    print ff


except KeyboardInterrupt :
	print "Stopping sensor output"
	ser.write("stop all"+"\r\n")
	print "Closing serial port" 
	ser.close()

