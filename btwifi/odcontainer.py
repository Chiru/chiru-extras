import csv
from collections import defaultdict, Counter
from datetime import datetime

#locationreader = csv.reader(open('clocations.csv', 'rb'), delimiter=',')
#codreader = csv.reader(open('cod.csv', 'rb'), delimiter=',')
#locationreader = csv.reader(open('clocationscrn.csv', 'rb'), delimiter=',') #Fixed enter and exit nodes
#codreader = csv.reader(open('odcorn.csv', 'rb'), delimiter=',') ##Fixed enter and exit nodes


#loclist = []
#locdict = {}
#codlist = []

class OriginContainer(object):

    def __init__(self):

        self.originweight = {}
        self.od = defaultdict(list)
        self.number_of_agents = 0
        self.loclist = []
        self.locdict = {}
        self.codlist = []

        #self.locationreader = csv.reader(open('clocations.csv', 'rb'), delimiter=',')
        #self.codreader = csv.reader(open('cod.csv', 'rb'), delimiter=',')

        self.locationreader = csv.reader(open('clocationscrn.csv', 'rb'), delimiter=',') #Fixed enter and exit nodes
        self.codreader = csv.reader(open('odcorn.csv', 'rb'), delimiter=',') ##Fixed enter and exit nodes


        for row in self.locationreader:
            self.loclist.append([int(row[0]),float(row[1]),float(row[2])])
            self.locdict[int(row[0])]=[float(row[1]),float(row[2])]

        for row in self.codreader:
            self.codlist.append(row)

    def update_weights(self,day,hour):
        #print day, hour
        #print codlist[0]
        #global number_of_agents
        #global destweight
        #global originweight
        #print 'wat'
        #print day,hour
        od = defaultdict(list)
        origins = []
        i = 0
        for f in self.codlist:
            #print str(day), f[0],str(hour),f[1]
            #date = datetime.strptime(f[0],'%Y-%m-%d')
            #print day,date
            #if day == date and str(hour) == f[1]:
            if day == f[0] and str(hour) == f[1]:
                #print "wat"
                origins.append(int(f[2]))
                od[f[2]].append([int(f[3]),int(f[4])])
                #destweight[codlist[i][2]].append([codlist[i][3],codlist[i][4]])
                i = i+1 #Experiment with this
            #print od
            #for key, value in od.iteritems():
                #destweight[key].append(Counter(value))
        self.originweight = Counter(origins)
            #number_of_agents = len(od)
        self.number_of_agents = i/2
        self.od = od
        #return origins, od, number_of_agents
        #return originweight, od, number_of_agents
            #destweight = od #Whaaat
            #number_of_agents = len(destweight)
            #print "Origins and their weights:", originweight
            #print "Origins with destinations and weights", od
            #print destweight
            #print "Agents: ", number_of_agents

    def get_origins(self):
        return self.originweight

    def get_od(self):
        return self.od

    def get_pedno(self):
        return self.number_of_agents

    def get_all_locations(self):
        return self.locdict

    def get_all_od(self):
        return self.codlist

    def get_all_loc(self):
        return self.loclist
