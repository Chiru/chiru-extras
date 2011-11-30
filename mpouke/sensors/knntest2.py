import math
import csv
import serial
from time import sleep

#dataset=csv.reader(open('data.csv'), delimiter=',')

output = csv.writer(open('data.csv', 'a'), delimiter=',')
dataset= csv.reader(open('data.csv'), delimiter=',')
port = "/dev/rfcomm0"
ser = serial.Serial(port, baudrate=9600, timeout=10)
global wholedata

#for row in dataset: print row

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
#ser.write("echo on"+"\r\n")      # write a string
ser.write("hello"+"\r\n")
ser.write("sett 114500000"+"\r\n")
ser.write("ags +000005000 100 1 0"+"\r\n")
print ser.portstr 

while True:
    print "Application for recording and testing short gestures"
    print "Select the action you wish to teach:"
    print "Type 1 for: Up"
    print "Type 2 for: Down"
    print "Type 3 for: Left"
    print "Type 4 for: Right"
    print "Type 5 for: Forwards"
    print "Type 6 for: Backwards"
    print "Type 7 for: Still"
    print "Type 8 to test classification"
    print "Type 0 to exit"
    
    selection = raw_input()

    if selection == '1':
    	    print "Get ready for 'Up in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
            
	    for r in range(10):
		    vector=[]
		    data = ser.readline()
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 3:
			line = vector[-6:]
			iline = [int(n) for n in line]
			iline.append('Up')
			output.writerow(iline)
			data=vectorcreate()
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result
		   	print iline

    elif selection == '2':
	    print "Get ready for 'Down' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"

	    for r in range(10):
		    vector=[]
		    data = ser.readline()
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 3:
			line = vector[-6:]
			iline = [int(n) for n in line]
			iline.append('Down')
			output.writerow(iline)
			data=vectorcreate()
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result
			print iline

    elif selection == '3':
	    print "Get ready for 'Left in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
	    for r in range(10):
		    vector=[]
		    data = ser.readline()
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 3:
			line = vector[-6:]
			iline = [int(n) for n in line]
			iline.append('Left')
			output.writerow(iline)
			data=vectorcreate()
			print iline
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result

    elif selection == '4':
	    print "Get ready for 'Left in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
	    for r in range(10):
		    vector=[]
		    data = ser.readline()
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 3:
			line = vector[-6:]
			iline = [int(n) for n in line]
			iline.append('Right')
			output.writerow(iline)
			data=vectorcreate()
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result

    elif selection == '5':
	    print "Get ready for 'Left in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
	    for r in range(10):
		    vector=[]
		    data = ser.readline()
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 3:
			line = vector[-6:]
			iline = [int(n) for n in line]
			iline.append('Forwards')
			output.writerow(iline)
			data=vectorcreate()
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result

    elif selection == '6':
	    print "Get ready for 'Left in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
	    for r in range(10):
		    vector=[]
		    data = ser.readline()
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 3:
			line = vector[-6:]
			iline = [int(n) for n in line]
			iline.append('Backwards')
			output.writerow(iline)
			data=vectorcreate()
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result

    elif selection == '7':
            print "Hold the sensor still in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
	    for r in range(20):
		    vector=[]
		    data = ser.readline()
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 3:
			line = vector[-6:]
			iline = [int(n) for n in line]
			iline.append('Still')
			output.writerow(iline)
			data=vectorcreate()
			print iline
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result
		    
    elif selection == '8':
	    data=vectorcreate()
	    print data
	    if len(data)==0:
		print "No teaching data present!"
		continue
	    else:
		vector=[]
		data = ser.readline()
		data = data.split(",")
		for i in data:
		 	i=i.rstrip("\r\n")
			vector.append(i)
		if len(vector) > 3:
			line = vector[-6:]
			iline = [int(n) for n in line]
			#iline.append('Up')
			#output.writerow(iline)
		   	result=knntest2.knnestimate(data,iline)
			print result

    elif selection == '0':
	    print "Exiting..."
	    break
	    
ser.write("stop all"+"\r\n")
print "Stopping sensor output"
ser.close()
print "Closing serial port connection, sensor light should turn from blue to green"

