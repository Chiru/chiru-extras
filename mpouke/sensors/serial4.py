import serial
from time import sleep
#import datetime
import csv

output = csv.writer(open('accdata.csv', 'wb'), delimiter=',')

port = "/dev/rfcomm0"
ser = serial.Serial(port, baudrate=9600, timeout=10)
print "connecting..."
sleep(2)
ser.write("echo on"+"\r\n")      # write a string
#ser.write("echo on"+"\r\n")      # write a string
ser.write("hello"+"\r\n")
ser.write("sett 114500000"+"\r\n")
ser.write("sens +000005000 100 1 500"+"\r\n")
print ser.portstr 

while True:
    vector=[]
    #print "Got here"
    data = ser.readline()
    print "Read line"
    data = data.split(",")
    for i in data:
    	i=i.rstrip("\r\n")
	vector.append(i)
    if len(vector) > 3:
	line = vector[-3:]
        print vector[-3:]
	output.writerow(line)

    #sleep(0.5)
    #print 'not blocked'

ser.close()

