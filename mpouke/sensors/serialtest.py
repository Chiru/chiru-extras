import serial
port = "/dev/rfcomm0"
ser = serial.Serial(port)  # open first serial port
print ser.portstr       # check which port was really used
ser.write("echo on")      # write a string
ser.write("hello")
ser.close()             # close port

