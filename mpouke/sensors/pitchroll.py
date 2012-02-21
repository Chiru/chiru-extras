import serial
import numpy as np
import math
from time import sleep

port = "/dev/rfcomm1"
ser = serial.Serial(port, baudrate=9600, timeout=10)
print "connecting..."
sleep(2)
ser.write("echo on"+"\r\n")      # write a string
#ser.write("echo on"+"\r\n")      # write a string
ser.write("stop all"+"\r\n")
ser.write("sett 114500000"+"\r\n")
ser.write("sens +000005000 100 1 0"+"\r\n")
print ser.portstr

def pitch(x,y,z,):
    #x = float(x)
    #y = float(y)
    #z = float(z)
    p = np.arctan(x/np.sqrt((y**2)+(z**2)))
    return p

def roll(x,y,z):
    #x = float(x)
    #y = float(y)
    #z = float(z)
    r = np.arctan(y/np.sqrt((x**2)+(z**2)))
    return r

while True:
    vector=[]
    #print "Got here"
    data = ser.readline()
    #print "Read line"
    data = data.split(",")
    for i in data:
    	i=i.rstrip("\r\n")
	vector.append(i)
    if len(vector) > 3:
	line = vector[-3:]
	iline = [float(n) for n in line]
	x=iline[0]
	y=iline[1]
	z=iline[2]
	#print 'X: ',x,' Y: ',y,' Z: ',z 
        #print vector[-6:]
	#output.writerow(line)
   	#result=knndir.knnestimate(knndir.data,iline)
	pt = pitch(x,y,z)
	rl = roll(x,y,z)
	print 'Pitch: ',np.degrees(pt)*-1, ' Roll: ',np.degrees(rl)*-1
	#print ' Roll: ',rl
    #sleep(0.5)
    #print 'not blocked'

print "Stopping sensor output"
ser.write("stop all"+"\r\n")
print "Closing serial port" 
ser.close()
