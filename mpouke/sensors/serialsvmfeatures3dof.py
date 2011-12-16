import serial
from time import sleep
#import datetime
#import csv
#import svmcomplete
import svmclassifierfeat
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
ser.write("sens +000005000 5 1 0"+"\r\n")
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

def energy(vect):
	v = vect
	npfeature = numpy.asarray(v)
	#print npfeature
	b = abs(npfeature)
	a = b**2
	#e=sum(abs(feature)**2)
	e = sum(a)
	#print npfeature
	return e

def flatten(lst):
    for elem in lst:
        if type(elem) in (tuple, list):
            for i in flatten(elem):
                yield i
        else:
            yield elem

def wavelet(vect):
	wav = vect
	wp = pywt.WaveletPacket(data=wav, wavelet='db3', mode='sym')
	aaa = wp['aaa'].data
	a = aaa.tolist()
	#print aaa
	ff = numpy.fft.fft(a)
	#print ff
	ff = abs(ff)
	f = ff.tolist()
	#print len(f)
	return f

try:

	while True:
	    buffer = ser.read(ser.inWaiting())
	    featureax=[]
	    featureay=[]
	    featureaz=[]
	    
	    allfeatures=[]
	    energies=[]
	    wavelets=[]
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
			ax = vector[-3]
			ay = vector[-2]
			az = vector[-1]
			
			featureax.append(float(ax))
			featureay.append(float(ay))
			featureaz.append(float(az))
			
	    if len(featureax)==64:
		    eax = energy(featureax)
		    eay = energy(featureay)
	  	    eaz = energy(featureaz)
		    
		    wavax = wavelet(featureax)
		    wavay = wavelet(featureay)
		    wavaz = wavelet(featureaz)
		    
		    energies.extend([eax,eay,eaz])
		    wavelets.extend([wavax,wavay,wavaz])
		    #print energies
	            wva = list(flatten(wavelets))
	            allfeatures.extend([energies, wva])
	
	    	    af = list(flatten(allfeatures))
		    result = svmclassifierfeat.classify(af)
		    print result
		    #print af
		    #print len(af)


except KeyboardInterrupt :
	print "Stopping sensor output"
	ser.write("stop all"+"\r\n")
	print "Closing serial port" 
	ser.close()
