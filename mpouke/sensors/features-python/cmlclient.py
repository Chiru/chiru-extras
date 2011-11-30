#sehr einfacher Commandline client zum auslesen der Sensor Daten
#ueber TCP
import socket
import numpy
HOST = 'localhost'    # The remote host
PORT = 7777
# oeffnen eines Sockets           
inS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
inS.connect((HOST, PORT))
i =0
while True:
    #Einlesen der Daten 
    #der Receive buffer wird auch gleich als Window fuer 
    #feature calc benutzt ... deswegen auch einmal mit versch. wsize rumspielen
    data = inS.recv(6024)
    i= i+1;
    if len(data) > 0:   
        split=data.split('\n');
        l = len(split[1])
        b = numpy.array([]);
        for s in split:
            if len(s)== l and len(s) !=0:
                line =s.split('\t')
                i = 0
                for elm in line:
                    line[i] = int(elm)
                    i = i + 1;
                a=numpy.array(line)
                b =numpy.append(b,a,axis=2)
        b.shape=(-1,12)
        #print b[:,2]
        if len(b) > 0:
#Beispiel Berrechnungen
#auf der beschleunigungssensor x achse die Varianz
            varx = b[:,2].var()
#auf der y achse etc.
            vary = b[:,3].var()
            meanx =numpy.mean(b[:,3])
            mediany =numpy.median(b[:,3])
            medianz =numpy.median(b[:,4])
            stdz = numpy.std(b[:,4])
            gmeanx=numpy.mean(b[:,5])
            gvarz = numpy.var(b[:,7])
            gmeany=numpy.mean(b[:,6])
            print meanx 
            



