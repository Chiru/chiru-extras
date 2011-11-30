
""" receiving OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation

this is a very basic example, for detailed info on pyOSC functionality check the OSC.py file 
or run pydoc pyOSC.py. you can also get the docs by opening a python shell and doing
>>> import OSC
>>> help(OSC)
"""


import OSC
import time, threading
import tetris_tk

LEFT = "left"
RIGHT = "right"
DOWN = "down"

# tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
receive_address = '127.0.0.1', 12000


# OSC Server. there are three different types of server. 
s = OSC.OSCServer(receive_address) # basic
##s = OSC.ThreadingOSCServer(receive_address) # threading
##s = OSC.ForkingOSCServer(receive_address) # forking



# this registers a 'default' handler (for unmatched messages), 
# an /'error' handler, an '/info' handler.
# And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
s.addDefaultHandlers()



# define a message-handler function for the server to call.
def printing_handler(addr, tags, stuff, source):
    print "---"
    print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"

def gesture_handler(addr, tags, stuff, source):
    #print "---"
    #print "received new osc msg from %s" % OSC.getUrlStr(source)
    #print "with addr : %s" % addr
    #print "typetags %s" % tags
    #print "data %s" % stuff
    if stuff[0] == 0:
	print 'Still'
    if stuff[0] == 1:
	print 'Right'
	tetris_tk.game_controller.right_callback
    if stuff[0] == 2:
	print 'Left'
	tetris_tk.game_controller.left_callback
    if stuff[0] == 3:
	print 'Forwards'
	tetris_tk.game_controller.down_callback
    if stuff[0] == 4:
	print 'Turn left'
    if stuff[0] == 5:
	print 'Turn right'
    #print "---"
    else: print stuff

s.addMsgHandler("/print", printing_handler) # adding our function
s.addMsgHandler("/OSCSynth/params", gesture_handler) # adding our function


# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
    print addr


# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = s.serve_forever )
st.start()


try :
    while 1 :
        time.sleep(5)

except KeyboardInterrupt :
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"
        
