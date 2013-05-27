import csv
from math import cos, radians
f = open('locations.txt', 'rb')
fw = open('clocations.csv','w')
cw = open('corners.csv','w')
f.next()
locations = csv.reader(f, delimiter=',')
lwriter = csv.writer(fw,delimiter=',')
cwriter = csv.writer(cw,delimiter=',')
center = [65.012962,25.472815]
#oulusize = [[-44,-206],[254,-12],[55,270],[-223,74]]
oulusize = [[-709,-571],[672,-569],[-707,712],[701,739]]
clocations = []
ne = []
nw = []
sw = []
se = []

def gpsToTundra(lat, lon):
    deltalat = center[0]-lat
    deltalon = center[1]-lon
    dispnorth = 1000*(deltalat*111.28)
    dispeast = -1000*(111.28*deltalon*cos(radians(lat)))
    return [dispeast,dispnorth]

def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside = False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

for row in locations:
    #print row[2],row[1]
    if row[1] == 'NULL': continue
    tcoords = gpsToTundra(float(row[2]),float(row[1]))#lon, lat
    if point_inside_polygon(tcoords[0],tcoords[1],oulusize):
        clocations.append([row[0],tcoords[0],tcoords[1]])
        continue
    if tcoords[0] > 0 and tcoords[1] < 0: ne.append([row[0],tcoords[0],tcoords[1]])
    if tcoords[0] < 0 and tcoords[1] < 0: nw.append([row[0],tcoords[0],tcoords[1]])
    if tcoords[0] < 0 and tcoords[1] > 0: sw.append([row[0],tcoords[0],tcoords[1]])
    if tcoords[0] > 0 and tcoords[1] > 0: se.append([row[0],tcoords[0],tcoords[1]])

for c in clocations:
    lwriter.writerow(c)

for n in ne:
    n.insert(0,'2001')
    cwriter.writerow(n)
for n in nw:
    n.insert(0,'2002')
    cwriter.writerow(n)
for n in sw:
    n.insert(0,'2004')
    cwriter.writerow(n)
for n in se:
    n.insert(0,'2003')
    cwriter.writerow(n)
       
#print clocations
