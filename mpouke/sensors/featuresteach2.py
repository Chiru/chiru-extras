import math
import csv
import serial
from time import sleep
import numpy
import pywt

#dataset=csv.reader(open('data.csv'), delimiter=',')

output = csv.writer(open('shortfeatures2.csv', 'a'), delimiter=',')
dataset= csv.reader(open('data.csv'), delimiter=',')
port = "/dev/rfcomm0"
ser = serial.Serial(port, baudrate=9600, timeout=10)
#global wholedata[]
#global vectorlist[]
#for row in dataset: print row

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
	#print len(aaa)
	a = aaa.tolist()
	print len(a)
	#return a
	#print aaa
	ff = numpy.fft.fft(a)
	#print ff
	ff = abs(ff)
	f = ff.tolist()
	return f


def vectorcreate():
	rows=[]
	for row in dataset:
		features=[]
		ftrs=row[0:6]
		for f in ftrs:
			features.append(int(f))
		label=row[6]
		rows.append({'features':features,'label':label})
	return rows

#data=vectorcreate()

#print actionlist[0:20]

def euclidean(v1,v2):
	d=0.0
	for i in range(len(v1)):
		d+=(v1[i]-v2[i])**2
	return math.sqrt(d)


#print data[0]['features'],data[873]['features']
#distance=euclidean(data[0]['features'],data[868]['features'])
#print ('Distance between ',data[0]['label'],' and ',data[868]['label'],' is: ',distance)

def getdistances(data,vec1):
	distancelist=[]
	for i in range(len(data)):
		vec2=data[i]['features']
		distancelist.append((euclidean(vec1,vec2),i))
	distancelist.sort()
	return distancelist

def knnestimate(data,vec1,k=5):
	#Get sorted distances
	dlist=getdistances(data,vec1)
	#avg=0.0
	classy=[]

	#Take the average of the top k results
	for i in range(k):
		idx=dlist[i][1]
		#avg+=data[idx]['label']
		classy.append(data[idx]['label'])
	#avg=avg/k
	#return avg
	return classy

#classification=knnestimate(data,data[0]['features'])
#print classification

print "connecting..."
sleep(2)
ser.write("echo on"+"\r\n")      # write a string
ser.write("sett 114500000"+"\r\n")
ser.write("ags +000005000 5 1 0"+"\r\n")
print ser.portstr 



while True:
    print "****************************************************"
    print "Application for recording direction (tilting) gestures"
    print "It takes 10 seconds to teach each direction gesture"
    print "****************************************************"
    print "Select the action you wish to teach:"
    print "Type 1 for: PushLeft"
    print "Type 2 for: PushRight"
    print "Type 3 for: PushForwards"
    print "Type 4 for: PushBackwards"
    print "Type 5 for: LargeCircleRight"
    print "Type 6 for: LargeCircleLeft"
    print "Type 7 for: Still (20 seconds)"
    print "Type 0 to exit"
    #dump = ser.readline()
    #print dump
    selection = raw_input()
    #buffer = ser.read(ser.inWaiting())

    if selection == '1':
    	    print "Get ready for 'PushLeft' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
            buffer = ser.read(ser.inWaiting())
	    for i in range (5):
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
			    wavelets.extend([wavax,wavay,wavaz,wavgx,wavgy,wavgz])
			    print energies
			    wva = list(flatten(wavelets))
			    allfeatures.extend([energies, wva])
	
		    	    af = list(flatten(allfeatures))
			    af.append('PushLeft')
			    print af
			    output.writerow(af)

    elif selection == '2':
    	    print "Get ready for 'PushRight' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
            buffer = ser.read(ser.inWaiting())
	    for i in range (5):
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
			    wavelets.extend([wavax,wavay,wavaz,wavgx,wavgy,wavgz])
			    print energies
			    wva = list(flatten(wavelets))
			    allfeatures.extend([energies, wva])
	
		    	    af = list(flatten(allfeatures))
			    af.append('PushRight')
			    print af
			    output.writerow(af)

    elif selection == '3':
    	    print "Get ready for 'PushForwards' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
            buffer = ser.read(ser.inWaiting())
	    for i in range (5):
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
			    wavelets.extend([wavax,wavay,wavaz,wavgx,wavgy,wavgz])
			    print energies
			    wva = list(flatten(wavelets))
			    allfeatures.extend([energies, wva])
	
		    	    af = list(flatten(allfeatures))
			    af.append('PushForwards')
			    print af
			    output.writerow(af)

    elif selection == '4':
    	    print "Get ready for 'PushBackwards' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
            buffer = ser.read(ser.inWaiting())
	    for i in range (5):
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
			    wavelets.extend([wavax,wavay,wavaz,wavgx,wavgy,wavgz])
			    print energies
			    wva = list(flatten(wavelets))
			    allfeatures.extend([energies, wva])
	
		    	    af = list(flatten(allfeatures))
			    af.append('PushBackwards')
			    print af
			    output.writerow(af)

    elif selection == '5':
    	    print "Get ready for 'LargeCircleRight' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
            buffer = ser.read(ser.inWaiting())
	    for i in range (12):
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
			    wavelets.extend([wavax,wavay,wavaz,wavgx,wavgy,wavgz])
			    print energies
			    wva = list(flatten(wavelets))
			    allfeatures.extend([energies, wva])
	
		    	    af = list(flatten(allfeatures))
			    af.append('LargeCircleRight')
			    print af
			    output.writerow(af)

    elif selection == '6':
    	    print "Get ready for 'LargeCircleLeft' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
            buffer = ser.read(ser.inWaiting())
	    for i in range (12):
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
			    wavelets.extend([wavax,wavay,wavaz,wavgx,wavgy,wavgz])
			    print energies
			    wva = list(flatten(wavelets))
			    allfeatures.extend([energies, wva])
	
		    	    af = list(flatten(allfeatures))
			    af.append('LargeCircleLeft')
			    print af
			    output.writerow(af)

   
    elif selection == '7':
    	    print "Get ready for 'Still' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
            buffer = ser.read(ser.inWaiting())
	    for i in range (24):
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
			    wavelets.extend([wavax,wavay,wavaz,wavgx,wavgy,wavgz])
			    print energies
			    wva = list(flatten(wavelets))
			    allfeatures.extend([energies, wva])
	
		    	    af = list(flatten(allfeatures))
			    af.append('Still')
			    print af
			    output.writerow(af)

    elif selection == '0':
	    print "Exiting..."
	    break
	    
ser.write("stop all"+"\r\n")
print "Stopping sensor output"
ser.close()
print "Closing serial port connection, sensor light should turn from blue to green"

