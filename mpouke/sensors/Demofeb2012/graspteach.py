import math
import csv
import serial
from time import sleep

#dataset=csv.reader(open('data.csv'), delimiter=',')

output = csv.writer(open('graspgestures.csv', 'a'), delimiter=',')
#dataset= csv.reader(open('data.csv'), delimiter=',')
port = "/dev/rfcomm0"
ser = serial.Serial(port, baudrate=9600, timeout=10)

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
    print "Type 1 for: Grasp"
    print "Type 7 for: Still (20 seconds)"
    print "Type 0 to exit"
    #dump = ser.readline()
    #print dump
    selection = raw_input()
    #buffer = ser.read(ser.inWaiting())

    if selection == '1':
    	    print "Get ready for 'Grasp' in 3..."
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
			iline.append('Grasp')
			output.writerow(iline)
			#vectorlist.append(iline)
			#wholedata=vectorcreate()
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result
		   	print iline

   
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
