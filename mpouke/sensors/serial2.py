import serial
from time import sleep

port = "/dev/rfcomm0"
ser = serial.Serial(port)
ser.write("echo on")      # write a string
ser.write("hello")

while True:
    data = ser.read(9999)
    if len(data) > 0:
        print 'Got:', data

    sleep(0.5)
    print 'not blocked'

ser.close()

