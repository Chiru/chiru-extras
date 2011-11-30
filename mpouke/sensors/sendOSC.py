import OSC
import time, random

def sendOSC(features):
	client = OSC.OSCClient()
	client.connect( ('127.0.0.1', 6448) ) # note that the argument is a tupple and not two arguments
	msg = OSC.OSCMessage() #  we reuse the same variable msg used above overwriting it
	msg.setAddress("/oscCustomFeatures")
	#msg.append("/oscCustomFeatures")
	msg.append(features)
	client.send(msg) # now we dont need to tell the client the address anymore


