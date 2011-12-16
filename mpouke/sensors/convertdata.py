import serial
from time import sleep
#import datetime
import csv
#import svmcomplete
import numpy
import pywt
rawdata = csv.writer(open('shortincreased.csv', 'rb'), delimiter=',') 
output = csv.writer(open('shortfeatures.csv', 'wb'), delimiter=',')

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


	    

allfeatures=[]
energies=[]
wavelets=[]
for row in rawdata:
	for i in range(64):
	featureax=[]
	featureay=[]
	featureaz=[]
	featuregx=[]
	featuregy=[]
	featuregz=[]
	
		vector=[]
		#print "Got here"
	
		#print "Read line"
		if len(vector) == 7:
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
		wva = list(flatten(wavelets))
		wva /= numpy.max(numpy.abs(wva),axis=0)
		w = wva.tolist()
		energies /= numpy.max(numpy.abs(energies),axis=0)
		allfeatures.extend([energies, w])
		af = list(flatten(allfeatures))
		print af
		print len(af)


