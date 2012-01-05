import math
import csv
import serial
from time import sleep

#dataset=csv.reader(open('data.csv'), delimiter=',')

output = csv.writer(open('shortgestures2.csv', 'a'), delimiter=',')

port = "/dev/rfcomm0"
ser = serial.Serial(port, baudrate=9600, timeout=10)
#global wholedata[]
#global vectorlist[]
#for row in dataset: print row


print "connecting..."
sleep(2)
ser.write("echo on"+"\r\n")      # write a string
ser.write("sett 114500000"+"\r\n")
ser.write("ags +000005000 100 1 0"+"\r\n")
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
    print "Type 6 for: Shake"
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
	    for r in range(5):
		    vector=[]
		    data = ser.readline()
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 3:
			line = vector[-6:]
			iline = [int(n) for n in line]
			iline.append('PushLeft')
			output.writerow(iline)
			#vectorlist.append(iline)
			#wholedata=vectorcreate()
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result
		   	print iline

    elif selection == '2':
	    print "Get ready for 'PushRight' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
	    buffer = ser.read(ser.inWaiting())
	    for r in range(5):
		    vector=[]
		    data = ser.readline()
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 3:
			line = vector[-6:]
			iline = [int(n) for n in line]
			iline.append('PushRight')
			output.writerow(iline)
			#wholedata=vectorcreate()
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result
			print iline

    elif selection == '3':
	    print "Get ready for 'PushForwards' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
	    buffer = ser.read(ser.inWaiting())
	    for r in range(5):
		    vector=[]
		    data = ser.readline()
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 3:
			line = vector[-6:]
			iline = [int(n) for n in line]
			iline.append('PushForwards')
			output.writerow(iline)
			#wholedata=vectorcreate()
			print iline
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result

    elif selection == '4':
	    print "Get ready for 'PushBackwards' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
	    buffer = ser.read(ser.inWaiting())
	    for r in range(5):
		    vector=[]
		    data = ser.readline()
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 3:
			line = vector[-6:]
			iline = [int(n) for n in line]
			iline.append('PushBackwards')
			output.writerow(iline)
			print iline
			#vectorlist.append(iline)
			#wholedata=vectorcreate()
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result

    elif selection == '5':
	    print "Get ready for 'LargeCircleRight' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
	    buffer = ser.read(ser.inWaiting())
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
			iline.append('LargeCircleRight')
			output.writerow(iline)
			print iline
			#vectorlist.append(iline)
			#wholedata=vectorcreate()
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result

    elif selection == '6':
	    print "Get ready for 'Shake' in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
	    buffer = ser.read(ser.inWaiting())
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
			iline.append('Shake')
			output.writerow(iline)
			print iline
			#vectorlist.append(iline)
			#wholedata=vectorcreate()
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
	    buffer = ser.read(ser.inWaiting())
	    for r in range(200):
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
			#wholedata=vectorcreate()
			print iline
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result


    elif selection == '0':
	    print "Exiting..."
	    break
	    
ser.write("stop all"+"\r\n")
print "Stopping sensor output"
ser.close()
print "Closing serial port connection, sensor light should turn from blue to green"

