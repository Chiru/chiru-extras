import serial
from time import sleep
#import datetime
import csv
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
	#print aaa
	ff = numpy.fft.fft(aaa)
	#print ff
	return ff

try:

	while True:
	    buffer = ser.read(ser.inWaiting())
	    featureax=[]
	    featureay=[]
	    featureaz=[]
	    featuregx=[]
	    featuregy=[]
	    featuregz=[]
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
			ax = vector[-6]
			ay = vector[-5]
			az = vector[-4]
			gx = vector[-3]
			gy = vector[-2]
			gz = vector[-1]
			featureax.append(float(ax))
			featureay.append(float(ay))
			featureaz.append(float(az))
			featuregx.append(float(gx))
			featuregy.append(float(gy))
			featuregz.append(float(gz))
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
	    #print featureax
	    #print len(featureax)
	    if len(featureax)==64:
		    eax = energy(featureax)
		    eay = energy(featureay)
	  	    eaz = energy(featureaz)
		    egx = energy(featuregx)
		    egy = energy(featuregy)
		    egz = energy(featuregz)
		    
		    wavax = wavelet(featureax)
		    wavay = wavelet(featureay)
		    wavaz = wavelet(featureaz)
		    wavgx = wavelet(featuregx)
		    wavgy = wavelet(featuregy)
		    wavgz = wavelet(featuregz)
	
		    energies.extend([eax,eay,eaz,egx,egy,egz])
		    wavelets.extend([wavax[:128],wavay[:128],wavaz[:128],wavgx[:128],wavgy[:128],wavgz[:128]])
		    #print eax
		    #print wavax[:128]
	            #a = [item for sublist in allfeatures for item in sublist]
		    print energies
		    #print wavelets
	            #print allfeatures
	            wva = list(flatten(wavelets))
		    #print wva
		    #allfeatures.extend([energies, wva])
	            wva /= numpy.max(numpy.abs(wva),axis=0)
		    w = wva.tolist()
		    energies /= numpy.max(numpy.abs(energies),axis=0)
		    allfeatures.extend([energies, w])
		    #print allfeatures
		    #feat = allfeatures.tolist()
		    #print allfeatures
		    #print len(allfeatures)
	    	    af = list(flatten(allfeatures))
		    #iline = af.tolist()
	  	    result=svmclassifierfeat.classify(af)
		    print result
		    #print len(af)


except KeyboardInterrupt :
	print "Stopping sensor output"
	ser.write("stop all"+"\r\n")
	print "Closing serial port" 
	ser.close()

