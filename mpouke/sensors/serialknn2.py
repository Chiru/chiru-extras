import serial
from time import sleep
#import datetime
import csv
import knntest2

output = csv.writer(open('data.csv', 'wb'), delimiter=',')

port = "/dev/rfcomm0"
ser = serial.Serial(port, baudrate=9600, timeout=10)
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
    print "Type 7 to test classification"
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
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result
		   print "Done"

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
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result

    elif selection == '3':
	    print "Get ready for 'Left in 3..."
	    sleep(1)
	    print "2..."
	    sleep(1)
	    print "1..."
            sleep(1)
            print "GO!!!"
	    for r in range(10)
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
		   	#result=knntest2.knnestimate(knntest2.data,iline)
			#print result

    elif selection == '4':

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
	   	#result=knntest2.knnestimate(knntest2.data,iline)
		#print result

    elif selection == '5':

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
	   	#result=knntest2.knnestimate(knntest2.data,iline)
		#print result

    elif selection == '6':

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
	   	#result=knntest2.knnestimate(knntest2.data,iline)
		#print result
	    
    elif selection == '7':
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
	   	result=knntest2.knnestimate(knntest2.data,iline)
		print result

    elif selection == '0':
	    continue
	    
ser.write("stop all"+"\r\n")
ser.close()

