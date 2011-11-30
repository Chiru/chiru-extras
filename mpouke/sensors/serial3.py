import serial
from time import sleep
import datetime

port = "/dev/rfcomm0"
ser = serial.Serial(port, timeout=500)
ser.write("echo on"+"\r\n")      # write a string
ser.write("hello"+"\r\n")
ser.write("sett 114500000"+"\r\n")
ser.write("sens +000005000 100 1 500"+"\r\n")


while True:
    data = ser.readline()
    data = data.split(",")
    for i in data:
    	i=i.rstrip("\\r\\n")
	#print i
    if len(data) > 0:
	line = data[-3:]
        print data[-3:]

    #sleep(0.5)
    #print 'not blocked'

ser.close()

