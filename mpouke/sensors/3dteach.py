import math
import csv
import serial
from time import sleep

#dataset=csv.reader(open('data.csv'), delimiter=',')

output = csv.writer(open('3dgestures.csv', 'a'), delimiter=',')
port = "/dev/rfcomm0"
ser = serial.Serial(port, baudrate=9600, timeout=10)
#global wholedata[]
#global vectorlist[]
#for row in dataset: print row


print "connecting..."
sleep(2)
ser.write("echo on"+"\r\n")      # write a string
ser.write("sett 114500000"+"\r\n")
ser.write("sens +000005000 10 1 0"+"\r\n")
print ser.portstr 

while True:
    print "****************************************************"
    print "Application for recording stuff, press 1 when ready "
    print "150 samples each"
    print "****************************************************"
    #dump = ser.readline()
    #print dump
    selection = raw_input()
    #buffer = ser.read(ser.inWaiting())

    if selection == '1':
    	    print "Get ready to record in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
            buffer = ser.read(ser.inWaiting())
	    for r in range(150):
		    vector=[]
		    data = ser.readline()
		    data = data.split(",")
		    for i in data:
		    	i=i.rstrip("\r\n")
			vector.append(i)
		    if len(vector) > 3:
			line = vector[-3:]
			iline = [int(n) for n in line]
			iline.append('Gesture')
			output.writerow(iline)
			#vectorlist.append(iline)
			#wholedata=vectorcreate()
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result
		   	print iline


    elif selection == '0':
	    print "Exiting..."
	    break
	    
ser.write("stop all"+"\r\n")
print "Stopping sensor output"
ser.close()
print "Closing serial port connection, sensor light should turn from blue to green"
