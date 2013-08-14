import pandas as pd
from datetime import timedelta
from collections import defaultdict

locations = pd.read_csv('btid.csv', parse_dates=True)
dataset = pd.read_csv('datatest.csv', parse_dates=True)
btindex = []
btid = []
dt = pd.datetime(2010, 7, 28)

for l in locations.Time:
    #print f
    hours = pd.datetime.fromtimestamp(l/1000.0)
    correct = pd.datetime.combine(dt,hours.time())
    #print correct - timedelta(hours=9)
    btindex.append(correct - timedelta(hours=9))

locations.index = btindex
#print btindex
print locations.Time

locindex = 0
loc = locations.ix[0][1]
start = True
for i in dataset.index:
    if locindex >= len(locations.index)-1:
        #print 'wat'
        #print loc
        btid.append(loc)
        continue
    print '******'
    loc = locations.ix[locindex][1]
    btid.append(loc)
    print loc
    time = dataset.Time[i]
    #print time
    try:
        time = pd.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        #print 'No milliseconds'
        time = pd.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    if start == True: time2 = locations.index[locindex]
    if start == False: time2 = locations.index[locindex+1]
    print 'dataset time: ',time
    print 'location time: ',time2
    delta = time2-time
    #print delta
    if delta.total_seconds() <0:
        print 'UPDATING'
        start = False     
        locindex = locindex +1    
        
print len(btid)
print len(dataset.index)

locseries = pd.DataFrame(btid,index=dataset.Time,columns=['Locations'])
print locseries
locdict = defaultdict(list)

for f in range(len(locseries.Locations)):
    #print locseries[f]
    if dataset.Annotations[f] in locdict[locseries.Locations[f]]: continue
    locdict[locseries.Locations[f]].append(dataset.Annotations[f])

print locdict


locseries.to_csv('locations.csv')
