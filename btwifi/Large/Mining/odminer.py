import csv
from math import cos, radians
f = open('clocations.csv', 'rb')
od = open('t.txt', 'rb')
ow = open('cod.csv','w')
cr = open('corners.csv','rb')
ocorn = open('odcorn.csv','w')
cornreader = csv.reader(cr, delimiter=',')
creader = csv.reader(f, delimiter=',')
odmatrix = csv.reader(od, delimiter=',')
odwriter = csv.writer(ow,delimiter=',')
odcornwriter = csv.writer(ocorn,delimiter=',')
clocations = []
odm = []
cornersonly = [] #trying to add enter and exit nodes
cornersall = [] #trying to add enter and exit nodes
odc = []


for row in creader:
    clocations.append(row[0])

for row in cornreader:
    cornersall.append(row)
    cornersonly.append(row[1])

for row in odmatrix:
    if row[2] in clocations and row[3] in clocations:
        odm.append(row)
        odc.append(row)
        continue
    if row[2] in clocations and row[3] in cornersonly:
        obs = [row[0],row[1],row[2],cornersall[cornersonly.index(row[3])][0],row[4]]
        odc.append(obs)
        continue
        #print row   
    if row[3] in clocations and row[2] in cornersonly:
        #print row
        #print 'Cornernode ',cornersall[cornersonly.index(row[2])][0]
        obs = [row[0],row[1],cornersall[cornersonly.index(row[2])][0],row[3],row[4]]
        odc.append(obs)

#print odc
for o in odm:
    odwriter.writerow(o)        
#print clocations

for o in odc:
    odcornwriter.writerow(o)
