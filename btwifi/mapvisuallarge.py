import os, sys
import pygame
from pygame.locals import *
import mesh_grid5
import csv
from math import *
import Pedestrian
from collections import Counter, defaultdict
import random
import time
from datetime import date, datetime, timedelta
import odcontainer

w = 1500                 #set width of screen
#h = 864                 #set height
h = 1080
screen = pygame.display.set_mode((w, h)) #make screen
pygame.font.init()
running = 1
global ORIGINX, ORIGINY
global ZOOM
BTCAPTURE = False
RANDOMCAPTURE = False #Remember to se Random mode in Pedestrian class
COMPARISONMODE = False
BTLARGECAPTURE = False
RANDOMLARGECAPTURE = True #Remember to se Random mode in Pedestrian class
ZOOM = 2
ORIGINX = screen.get_width()/2 #move origin 
ORIGINY = (screen.get_height()-100)/2 #move origin
black = 0, 0, 0
#clock = pygame.time.Clock()
colorscheme = [[255, 255, 217],[237, 248, 217],[199, 233, 180],[127, 205, 187],[65, 182, 196],[29, 145, 192],[34, 94, 168],[37, 52, 148],[8, 29, 88]]
#heatscheme = [[215, 48, 39],[244, 109, 67],[253, 174, 97],[254, 224, 139],[255, 255, 191],[217, 239, 139],[166, 217, 106],[102, 189, 99],[26, 152, 80]]
#heatscheme = [[255, 245, 240],[254, 224, 210],[252, 187, 161],[252, 146, 114],[251, 106, 74],[239, 59, 44],[203, 24, 29],[165, 15, 21],[103, 0, 13]] 
#heatscheme = [[255, 255, 255],[240, 240, 240],[217, 217, 217],[189, 189, 189],[150, 150, 150],[115, 115, 115],[82, 82, 82],[37, 37, 37],[0, 0, 0]]
heatscheme = [[255, 255, 217],[237, 248, 217],[199, 233, 180],[127, 205, 187],[65, 182, 196],[29, 145, 192],[34, 94, 168],[37, 52, 148],[8, 29, 88]]
#bischeme = [[158, 1, 66], [213, 62, 79],[244, 109, 67],[253, 174, 97],[254, 224, 139],[255, 255, 191],[230, 245, 152],[171, 221, 164],[102, 194, 165],[50, 136, 189],[94, 79, 162]]
bischeme = [[165, 0, 38],[215, 48, 39],[244, 109, 67],[253, 174, 97],[254, 224, 139],[255, 255, 191],[217, 239, 139],[166, 217, 106],[102, 189, 99],[26, 152, 80],[0, 104, 55]]
#heatscheme = colorscheme
#colorscheme = [[255, 255, 204],[255, 237, 160],[254, 217, 118],[254, 178, 76],[253, 141, 60],[252, 78, 42],[227, 26, 28],[189, 0, 38],[128, 0, 38]]
colorscheme.reverse()
heatscheme.reverse()

if COMPARISONMODE == True: black = 255, 255, 255 #Setting black background to white
#center=[65.013012,25.472756]
center=[65.012962,25.472815]
nuke=[65.01211,25.47619]
willisika=[65.01085,25.473636]
north=[65.014278,25.473272]
stmichaels=[65.012817,25.474781]
#originweight = {}
#destweight = defaultdict(list)
number_of_agents = 0
oulusize = [[-44,-206],[254,-12],[55,270],[-223,74]]
allists = []
path = []
if BTCAPTURE == True:
    #For writing the visual weight data
    btvw = open('btvisualweights.csv','w') #Bluetooth wifi testing writing
    btwriter = csv.writer(btvw,delimiter=',') #Bluetooth wifi testing writing

if RANDOMCAPTURE == True: 
    rvw = open('rvisualweights.csv','w') #Random testing writing
    rwriter = csv.writer(rvw,delimiter=',') #Random testing writing

if COMPARISONMODE == True:
    btvr = open('btvisualweights.csv','r') #Bluetooth wifi testing
    rvr = open('rvisualweights.csv','r') #Random testing
    btreader = csv.reader(btvr,delimiter=',') #Bluetooth wifi testing
    rreader = csv.reader(rvr,delimiter=',') #Random testing

if BTLARGECAPTURE == True:
    morningbt = open('morningbt.csv','w')
    noonbt = open('noonbt.csv','w')
    afternoonbt = open('afternoonbt.csv','w')
    eveningbt = open('eveningbt.csv','w')
    nightbt = open('nightbt.csv','w')
    small_hoursbt = open('small_hoursbt.csv','w')
    morningwriter = csv.writer(morningbt,delimiter=',')
    noonwriter = csv.writer(noonbt,delimiter=',')
    afternoonwriter = csv.writer(afternoonbt,delimiter=',')
    eveningwriter = csv.writer(eveningbt,delimiter=',')
    nightwriter = csv.writer(nightbt,delimiter=',')
    small_hourswriter = csv.writer(small_hoursbt,delimiter=',')

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

def gpsToTundra(lat, lon):
    deltalat = center[0]-lat
    deltalon = center[1]-lon
    dispnorth = 1000*(deltalat*111.28)
    dispeast = -1000*(111.28*deltalon*cos(radians(lat)))
    return [dispeast,dispnorth]

def gps_raw(coord):
    tundralist=[]
    for c in coord:
         #print c
         tundralist.append(gpsToTundra(float(c[0]),float(c[1])))
    return tundralist

def loadOBJ(filename):  
    numVerts = 0  
    verts = []  
    faces = []  
    vertsOut = []  
    facesOut = []  
    for line in open(filename, "r"):  
        vals = line.split()  
        if vals[0] == "v":  
            v = map(float, vals[1:4])  
            verts.append(v)  
        #if vals[0] == "vn":  
        #    n = map(float, vals[1:4])  
        #    norms.append(n)  
        if vals[0] == "f":  
            for f in vals[1:]:  
                w = f.split()  
                # OBJ Files are 1-indexed so we must subtract 1 below  
                vertsOut.append(list(verts[int(w[0])-1]))  
                #normsOut.append(list(norms[int(w[2])-1]))  
                numVerts += 1  
    #return vertsOut, facesOut
    return vertsOut

def group(lst, n):
    return zip(*[lst[i::n] for i in range(n)])

def findCentroid2D(v1,v2,v3):
    x = (v1[0]+v2[0]+v3[0])/3
    y = (v1[1]+v2[1]+v3[1])/3
    #z = (v1[2]+v2[2]+v3[2])/3
    return(x,y)

def vdistsqr(a, b):
    x = b[0] - a[0] 
    y = b[1] - a[1]
    return sqrt(x * x + y * y)

def vequal(a, b):
    return vdistsqr(a, b) < (0.001 * 0.001)

vertlist = loadOBJ("largerdec.obj")

nodes = group(vertlist,3)
xynodes = []

def check_node(a):
    for n in xynodes:
        if point_inside_polygon(a[0],a[1],n):
            #print "Found"
            return True
    return False

def corner_side(a,b,c):
    # Check if point A lies left or right of the apex C
    ax = a[0]
    bx = b[0]
    ay = a[1]
    by = b[1]
    cx = c[0]
    cy = c[1]
    middlex = (ax+bx)/2
    middley = (ay+by)/2
    return ((middlex - cx)*(ay - cy) - (middley - cy)*(ax - cx)) > 0

for i in nodes:
    newnode=[]
    for v in i:
        xyvertex=[]
        xyvertex.append(v[0])
        xyvertex.append(v[2])
        newnode.append(xyvertex)
    xynodes.append(newnode)

if COMPARISONMODE == True:
    comparisondict = {}
    for x,y in zip(btreader,rreader):
        #print x,y
        comparisondict[int(x[0])]=int(y[1])-int(x[1])

#print 'Comparisondict should be coming out now'
#for key, value in comparisondict.iteritems(): print key,value
#print 'Well did it?'


nodevisual = {}
for node in range(len(xynodes)):
    nodevisual[node]=0

def draw_map():
    #COMPARISONMODE = False
    if COMPARISONMODE == True:
        for n in xrange(len(xynodes)):
            intnode = []
            for i in xynodes[n]:
                intnode.append([int(i[0])*ZOOM+ORIGINX,int(i[1])*ZOOM+ORIGINY])
            #print intnode
            #pygame.draw.circle(screen, (0, 255, 0), (int(n[0]), int(n[1])), 1)
            #if comparisondict[n] == 0: pygame.draw.polygon(screen, (100, 100,100), intnode, 1)
            # if comparisondict[n] > 0 and comparisondict[n] <= 4: pygame.draw.polygon(screen, heatscheme[0], intnode, 0)
            # if comparisondict[n] > 4 and comparisondict[n] <= 8: pygame.draw.polygon(screen, heatscheme[1], intnode, 0)
            # if comparisondict[n] > 8 and comparisondict[n] <= 12: pygame.draw.polygon(screen, heatscheme[2], intnode, 0)
            # if comparisondict[n] > 12 and comparisondict[n] <= 16: pygame.draw.polygon(screen, heatscheme[3], intnode, 0)
            # if comparisondict[n] > 16 and comparisondict[n] <= 20: pygame.draw.polygon(screen, heatscheme[4], intnode, 0)
            # if comparisondict[n] > 20 and comparisondict[n] <= 24: pygame.draw.polygon(screen, heatscheme[5], intnode, 0)
            # if comparisondict[n] > 24 and comparisondict[n] <= 30: pygame.draw.polygon(screen, heatscheme[6], intnode, 0)
            if comparisondict[n] < -50: pygame.draw.polygon(screen, bischeme[0], intnode, 0)
            if comparisondict[n] > -50 and comparisondict[n] <= -40: pygame.draw.polygon(screen, bischeme[1], intnode, 0)
            if comparisondict[n] > -40 and comparisondict[n] <= -30: pygame.draw.polygon(screen, bischeme[2], intnode, 0)
            if comparisondict[n] > -30 and comparisondict[n] <= -20: pygame.draw.polygon(screen, bischeme[3], intnode, 0)
            if comparisondict[n] > -20 and comparisondict[n] <= -10: pygame.draw.polygon(screen, bischeme[4], intnode, 0)
            if comparisondict[n] > -10 and comparisondict[n] < 0: pygame.draw.polygon(screen, bischeme[5], intnode, 0)
            if comparisondict[n] > 0 and comparisondict[n] <= 10: pygame.draw.polygon(screen, bischeme[6], intnode, 0)
            if comparisondict[n] > 10 and comparisondict[n] <= 20: pygame.draw.polygon(screen, bischeme[7], intnode, 0)
            if comparisondict[n] > 20 and comparisondict[n] <= 30: pygame.draw.polygon(screen, bischeme[8], intnode, 0)
            if comparisondict[n] > 30 and comparisondict[n] <= 40: pygame.draw.polygon(screen, bischeme[9], intnode, 0)
            if comparisondict[n] > 40: pygame.draw.polygon(screen, bischeme[10], intnode, 0)

            #if comparisondict[n] > 30: pygame.draw.polygon(screen, heatscheme[7], intnode, 0)
            pygame.draw.polygon(screen, (100, 100,100), intnode, 1)

    else:
        for n in xrange(len(xynodes)):
            intnode = []
            for i in xynodes[n]:
                intnode.append([int(i[0])*ZOOM+ORIGINX,int(i[1])*ZOOM+ORIGINY])
            #print intnode
            #pygame.draw.circle(screen, (0, 255, 0), (int(n[0]), int(n[1])), 1)
            #if nodevisual[n] == 0: pygame.draw.polygon(screen, (100, 100,100), intnode, 1)
            # if nodevisual[n] > 0 and nodevisual[n] <= 4: pygame.draw.polygon(screen, heatscheme[0], intnode, 0)
            # if nodevisual[n] > 4 and nodevisual[n] <= 8: pygame.draw.polygon(screen, heatscheme[1], intnode, 0)
            # if nodevisual[n] > 8 and nodevisual[n] <= 12: pygame.draw.polygon(screen, heatscheme[2], intnode, 0)
            # if nodevisual[n] > 12 and nodevisual[n] <= 16: pygame.draw.polygon(screen, heatscheme[3], intnode, 0)
            # if nodevisual[n] > 16 and nodevisual[n] <= 20: pygame.draw.polygon(screen, heatscheme[4], intnode, 0)
            # if nodevisual[n] > 20 and nodevisual[n] <= 24: pygame.draw.polygon(screen, heatscheme[5], intnode, 0)
            # if nodevisual[n] > 24 and nodevisual[n] <= 30: pygame.draw.polygon(screen, heatscheme[6], intnode, 0)
            if nodevisual[n] > 0 and nodevisual[n] <= 10: pygame.draw.polygon(screen, heatscheme[0], intnode, 0)
            if nodevisual[n] > 10 and nodevisual[n] <= 20: pygame.draw.polygon(screen, heatscheme[1], intnode, 0)
            if nodevisual[n] > 20 and nodevisual[n] <= 30: pygame.draw.polygon(screen, heatscheme[2], intnode, 0)
            if nodevisual[n] > 30 and nodevisual[n] <= 40: pygame.draw.polygon(screen, heatscheme[3], intnode, 0)
            if nodevisual[n] > 40 and nodevisual[n] <= 50: pygame.draw.polygon(screen, heatscheme[4], intnode, 0)
            if nodevisual[n] > 50 and nodevisual[n] <= 60: pygame.draw.polygon(screen, heatscheme[5], intnode, 0)
            if nodevisual[n] > 60 and nodevisual[n] <= 70: pygame.draw.polygon(screen, heatscheme[6], intnode, 0)
            if nodevisual[n] > 70 and nodevisual[n] <= 80: pygame.draw.polygon(screen, heatscheme[7], intnode, 0)
            if nodevisual[n] > 80: pygame.draw.polygon(screen, heatscheme[8], intnode, 0)

            #if nodevisual[n] > 30: pygame.draw.polygon(screen, heatscheme[7], intnode, 0)
            pygame.draw.polygon(screen, (100, 100,100), intnode, 1)
        #pygame.display.flip()

def find_closest(a):
    distances = []
    for b in mesh_grid5.coords: 
        distances.append(vdistsqr(a, b))
    smallest = min(distances)
    return distances.index(smallest)

def find_closest_from_list(a,l):
    #print 'This is current:', a
    #print 'This is the list of closest', l
    distances = []
    coordinates = []
    for b in l:
        bc = mesh_grid5.coords[b]
        distances.append(vdistsqr(a, bc))
        coordinates.append(bc)
    smallest = min(distances)
    closest = coordinates[distances.index(smallest)]
    return closest

import heapq

def find_n_closest(a,n):
    distances = []
    nclosest = []
    for b in mesh_grid5.coords: 
        distances.append(vdistsqr(a, b))    
    nlesser_items = heapq.nsmallest(n, distances)
    for i in nlesser_items:
        nclosest.append(distances.index(i))
    return nclosest

    #sdist = distances.sort()
    #return distances[0:n]

def triarea(a,b,c):
    ax = b[0] - a[0]
    ay = b[1] - a[1]
    bx = c[0] - a[0]
    by = c[1] - a[1]
    return bx * ay - ax * by

def string_pull(route,portals):
    #apexindex = 0
    points=[]
    centerindex = 0
    leftIndex = 0
    rightIndex = 0
    apexIndex = 0
    portalApex = route[0]
    points.append(portalApex)
    i = 0
    if len(route) == 1: 
        #print "Short route, no funneling"
        return route
    if len(portals) == 0: print "Portal warning!",route
    isleft = corner_side(portals[0][0],portals[0][1],portalApex)
    if isleft:
        portalLeft = portals[0][0]
        portalRight = portals[0][1]
    else:
        portalLeft = portals[0][1]
        portalRight = portals[0][0]
    
    #currentfunnel = triarea(apex,currentleft,currentright)
    while i <= len(portals)-1:
    #for p in portals:
        p1 = portals[i][0]
        p2 = portals[i][1]
        c = route[i]
        #p1 = p[0]
        #p2 = p[1]
        #c = route[portals.index(p)]
        isleft = corner_side(p1,p2,c)
        if isleft:
            left = p1
            right = p2
        else:
            left = p2
            right = p1

        #Update right vertex.
        if triarea(portalApex, portalRight, right) <= 0.0:
            if vequal(portalApex, portalRight) or triarea(portalApex, portalLeft, right) > 0.0:
                #Tighten the funnel.
                portalRight = right
                rightIndex = i
            else:
                #Right over left, insert left to path and restart scan from portal left point.
                points.append(portalLeft)
                #Make current left the new apex.
                portalApex = portalLeft
                apexIndex = leftIndex
                #Reset portal
                portalLeft = portalApex
                portalRight = portalApex
                leftIndex = apexIndex
                rightIndex = apexIndex
                #Restart scan
                i = apexIndex
                #continue

        #Update left vertex.
        if triarea(portalApex, portalLeft, left) >= 0.0:
            if vequal(portalApex, portalLeft) or triarea(portalApex, portalRight, left) < 0.0:
                #Tighten the funnel.
                portalLeft = left
                leftIndex = i
            else:
                #Left over right, insert right to path and restart scan from portal right point.
                points.append(portalRight)
                #Make current right the new apex.
                portalApex = portalRight
                apexIndex = rightIndex
                #Reset portal
                portalLeft = portalApex
                portalRight = portalApex
                leftIndex = apexIndex
                rightIndex = apexIndex
                #Restart scan
                i = apexIndex
                #continue

        i = i+1

    points.append(route[-1])
    return points

        #newfunnel1 = triarea(apex,left,currentright)
        #newfunnel2 = triarea(apex,left,currentright)
        #if newfunnel < currentfunnel and newfunnel >0:
        #    leftindex = leftindex + 1
        #    currentleft = portals[leftindex][0]


        #funnel = triarea(left,right,apex)

def knn(point,points,k=12):
    avgx = 0.0
    avgy = 0.0
    dlist = []
    closest = []    
    for p in points:
        dlist.append([vdistsqr(point,[float(p[0]),float(p[1])]),points.index(p)])
    dlist.sort(key = lambda x: x[0])
    for f in range(k):
        #print f
        #print dlist[f]
        closest.append(points[dlist[f][1]])
    for c in closest:
        #print c[0]
        avgx += float(c[0])
        avgy += float(c[1])
    avgx = avgx/k 
    avgy = avgy/k
    avg=[avgx,avgy]
    return avg
            
def create_route(source,destination):
    a = mesh_grid5.find_node(source)
    b = mesh_grid5.find_node(destination)
    route = mesh_grid5.search_path(a,b)
    edges = mesh_grid5.search_portals(a,b)
    funnelpoints = string_pull(route,edges)
    return funnelpoints

def weighted_choice(choices):
   #print choices
   total = sum(w for c,w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto+w > r:
         return c
      upto += w
   assert False, "Shouldn't get here"

def fuzzy_destination(destination):
    fuzzylist = find_n_closest(destination,10)
    rc = random.choice(fuzzylist)
    #print "Fuzzy destination", random.choice(fuzzylist)
    return rc

def pick_first(origins):
    #origins = odmatrix.get_origins()
    locdict = odmatrix.get_all_locations()
    #print origins
    #print locdict
    locindex = weighted_choice(origins.items())
    target = locdict[int(locindex)]
    return locindex,fuzzy_destination(target)

def pick_second(current,od):
    #global destweight
    #print "whatta",current
    #print od
    #print od[str(current)]
    locdict = odmatrix.get_all_locations()
    locindex = weighted_choice(od[str(current)])
    target = locdict[int(locindex)]
    return locindex,fuzzy_destination(target)

spotroutes = []

def draw_route():
    tlist = gps_raw(gpslist)
    #a = 231
    a = mesh_grid5.random_target()
    b = mesh_grid5.random_target()
    #b = 1044
    anode = xynodes[a]
    bnode = xynodes[b]
    acoord = findCentroid2D(anode[0],anode[1],anode[2])
    bcoord = findCentroid2D(bnode[0],bnode[1],bnode[2])
    nuclear = gpsToTundra(nuke[0],nuke[1])
    sm = gpsToTundra(stmichaels[0],stmichaels[1])
    #print acoord,bcoord
    pygame.draw.circle(screen, (255, 0, 0), (int(acoord[0])*ZOOM+ORIGINX, int(acoord[1])*ZOOM+ORIGINY), 4)
    pygame.draw.circle(screen, (0, 255, 100), (int(bcoord[0])*ZOOM+ORIGINX, int(bcoord[1])*ZOOM+ORIGINY), 4)
    pygame.draw.circle(screen, (255, 255, 255), (int(sm[0])*ZOOM+ORIGINX, int(sm[1])*ZOOM+ORIGINY), 4)
    pygame.draw.circle(screen, (255, 255, 255), (int(nuclear[0])*ZOOM+ORIGINX, int(nuclear[1])*ZOOM+ORIGINY), 4)
    route = mesh_grid5.search_path(a,b)
    edges = mesh_grid5.search_portals(a,b)
    pygame.display.flip()
    if route:
        path = []
        funnelpoints = string_pull(route,edges)
        #print funnelpoints
        for f in funnelpoints:
            px = f[0]*ZOOM+ORIGINX
            py = f[1]*ZOOM+ORIGINY
            path.append([px,py])
        pygame.draw.lines(screen, (0, 255, 0), False, path, 2)
        for f in funnelpoints:
            pygame.draw.circle(screen, (0, 255, 100), (int(f[0])*ZOOM+ORIGINX, int(f[1])*ZOOM+ORIGINY), 4)
           
        #for r in route:
            #pygame.draw.circle(screen, (0, 255, 100), (int(r[0])*ZOOM+ORIGINX, int(r[1])*ZOOM+ORIGINY), 3)
    if tlist:
        for t in tlist:
            if not check_node(t):
                b = [0,0]
                b[0], b[1] = t[1], t[0]
                #print "What happens: ",t
                c = mesh_grid5.coords[find_closest(b)]
                pygame.draw.circle(screen, (255, 255, 255), (int(c[0])*ZOOM+ORIGINX, int(c[1])*ZOOM+ORIGINY), 3)
                pygame.draw.circle(screen, (100, 100, 100), (int(t[0])*ZOOM+ORIGINX, int(t[1])*ZOOM+ORIGINY), 3)
            #print "wat"
            #print t[0],t[1]
            else:
                pygame.draw.circle(screen, (50, 255, 50), (int(t[0])*ZOOM+ORIGINX, int(t[1])*ZOOM+ORIGINY), 3)
    if edges:
        for e in edges:
            e1 = e[0]
            e2 = e[1]
            c = route[edges.index(e)]
            isleft = corner_side(e1,e2,c)
            if isleft:
                left = e1
                right = e2
            else:
                left = e2
                right = e1

            pygame.draw.circle(screen, (255, 255, 255), (int(left[0])*ZOOM+ORIGINX, int(left[1])*ZOOM+ORIGINY), 2)
            pygame.draw.circle(screen, (100, 100, 255), (int(right[0])*ZOOM+ORIGINX, int(right[1])*ZOOM+ORIGINY), 2)     
            #pygame.draw.circle(screen, (255, 255, 255), (int(e[0][0])*ZOOM+ORIGINX, int(e[0][1])*ZOOM+ORIGINY), 2)
            #pygame.draw.circle(screen, (100, 100, 255), (int(e[1][0])*ZOOM+ORIGINX, int(e[1][1])*ZOOM+ORIGINY), 2)
            #pygame.draw.line(screen, (255,255,255), (int(e[0][0])*ZOOM+ORIGINX, int(e[0][1])*ZOOM+ORIGINY), (int(e[1][0])*ZOOM+ORIGINX, int(e[1][1])*ZOOM+ORIGINY), 2)

    pygame.display.flip()

def update_time(day,hour):
    #day = '2012-05-08'
    d = datetime.strptime(day,'%Y-%m-%d')
    #dstmp = time.strptime(day,"%Y-%m-%d")
    hour = hour + 1
    if hour == 24:
        hour = 0
        d = d+timedelta(days=1)
        #print str(d)
        day = d.strftime("%Y-%m-%d")
        #day = str(d)
    return day,str(hour)
    #return     
  
#print route

#starttime = time.time()
odmatrix = odcontainer.OriginContainer()
if __name__ == "__main__":
    day = '2012-05-01'
    #dstmp = time.strptime(day,"%Y-%m-%d")
    #print dstmp
    hour = '6' #Do not put leading zeros, e.g. use 8 instead of 08
    #origins, od, number_of_agents = odmatrix.update_weights(day,hour)
    odmatrix.update_weights(day,hour)
    origins = odmatrix.get_origins()
    #print origins
    od = odmatrix.get_od()
    number_of_agents = odmatrix.get_pedno()
    #print number_of_agents
    pedestrians = []
    frame = 0
    #peds = ['ped1','ped2','ped3','ped4','ped5','ped6','ped7','ped8','ped9','ped10','ped11','ped12']
    #for ped in peds:
        #ped = Pedestrian.Pedestrian()
        #ped.set_random_location()
        #ped.set_random_goal()
        #ped.set_path()
        #pedestrians.append(ped)

    for r in range(number_of_agents):
        r = Pedestrian.Pedestrian()
        r.set_random_location()
        r.destweights = od
        r.origins = origins
        hotspot, goal = pick_first(origins)
        r.hotspot = hotspot
        r.set_goal(goal)
        r.set_path()
        pedestrians.append(r)

    for pd in pedestrians:
        pd.neighbors.extend(pedestrians)
        pd.neighbors.remove(pd) 

pedestrian_simulation = True
mode = 0
stick = 0
while running and __name__ == "__main__":
    #clock.tick()
    stick += 1
    global mode
    global pedestrian_simulation
    #elapsed_time = time.time() - starttime
    #print elapsed_time
    #if elapsed_time > 600: #You can set the speed of time changes here
    if stick == 2400:
        #starttime = time.time()
        day,hour = update_time(day,int(hour))
        if BTLARGECAPTURE == True: towrite = day+hour+'.csv'
        if RANDOMLARGECAPTURE == True: towrite = 'r'+day+hour+'.csv'
        if hour == '10':
            print towrite
            writer = csv.writer(open(towrite,'w'),delimiter=',')
            for key,value in nodevisual.iteritems():
                writer.writerow([key,value])
                nodevisual[key]=0
        if hour == '14':
            print towrite
            writer = csv.writer(open(towrite,'w'),delimiter=',')
            for key,value in nodevisual.iteritems():
                writer.writerow([key,value])
                nodevisual[key]=0
        if hour == '18':
            print towrite
            writer = csv.writer(open(towrite,'w'),delimiter=',')        
            for key,value in nodevisual.iteritems():
                writer.writerow([key,value])
                nodevisual[key]=0
        if hour == '22':
            print towrite
            writer = csv.writer(open(towrite,'w'),delimiter=',')
            for key,value in nodevisual.iteritems():
                writer.writerow([key,value])
                nodevisual[key]=0
        if hour == '2':
            print towrite
            writer = csv.writer(open(towrite,'w'),delimiter=',')
            for key,value in nodevisual.iteritems():
                writer.writerow([key,value])
                nodevisual[key]=0
        if hour == '6':
            print towrite
            writer = csv.writer(open(towrite,'w'),delimiter=',')
            for key,value in nodevisual.iteritems():
                writer.writerow([key,value])
                nodevisual[key]=0
        if day == '2012-05-31':
            print 'It seems that everything went ok'
            running = 0

        odmatrix.update_weights(day,hour)
        origins = odmatrix.get_origins()
        #print origins
        od = odmatrix.get_od()
        number_of_agents = odmatrix.get_pedno()
        for ped in pedestrians:
            ped.destweights = od
            ped.origins = origins
        stick = 0
        #print pedestrians[0].destweights
    #Set true if want animated pedestrians
    mpos = pygame.mouse.get_pos()
    xpos = (mpos[0]-ORIGINX)/ZOOM
    ypos = (mpos[1]-ORIGINY)/ZOOM
    frame = frame +1
    if frame == 1 and pedestrian_simulation == True:
        #fps = clock.get_fps()
        #print fps/20
        #screen.fill(black)
        #print "Simulating..."
        #mode = 3
        #screen.fill(black)
        #draw_map()
        #draw_gps()
        origins = odmatrix.get_origins()
        #print day,hour, origins
        locdict = odmatrix.get_all_locations()
        #print '**************************** This many origins: ',len(origins)
        for o in origins:
            omin = min(origins, key=origins.get)
            omax = max(origins, key=origins.get)
            #print omin
            #print omax
            minvalue = origins[omin]
            maxvalue = origins[omax]
            #print 'min: ',minvalue
            #print 'max: ',maxvalue
            x = locdict[o][0]
            y = locdict[o][1]
            #print "x: ",x
            #print "y: ",y
            ishift = origins[o]-minvalue
            # y = 1 + (x-A)*(10-1)/(B-A)
            #intensity = ishift*(255/(maxvalue-minvalue))
            intensity = ishift*8/(maxvalue-minvalue)
            #print 'intensity: ',intensity
            #print intensity
            pygame.draw.circle(screen, (colorscheme[intensity][0],colorscheme[intensity][1],colorscheme[intensity][2]),(int(x*ZOOM+ORIGINX), int(y*ZOOM+ORIGINY)), 5)
            #pygame.draw.circle(screen, (int(intensity),0,255-intensity), (int(x*ZOOM+ORIGINX), int(y*ZOOM+ORIGINY)), 5)
        pedestrians = [p for p in pedestrians if p.to_be_destroyed == False]
        if len(pedestrians) < number_of_agents:
            #print 'oeoe'
            entrys = []
            #print origins
            for key in origins:
                if key == 2001 or key == 2002 or key == 2003 or key == 2004: entrys.append([key,origins[key]])
            entry = weighted_choice(entrys)
            #if entry == 2001: portals = [[-36,-192],[35,-138],[131,-78],[235,-5]]
            #if entry == 2003: portals = [[235,-5],[178,68],[122,154],[59,244]]
            #if entry == 2004: portals = [[59,244],[-38,182],[-121,125],[-211,67]]
            #if entry == 2002: portals = [[-211,67],[-149,-26],[-97,-112],[-44,-192]]
            #if entry == 2001: portals = [[75,-560],[144,-560],[172,-560],[195,-561],[274,-559],[427,-558],[598,-560],[680,-460],[679,-429],[678,-392],[681,-232],[675,-160],[675,-106]] 
            #if entry == 2002: portals = [[-617,-561],[-218,-554],[-199,559],[-86,-560],[-356,-560],[-698,-474],[-696,-376]]
            #if entry == 2003: portals = [[681,26],[676,271],[677,384],[676,440],[264,713],[386,716],[427,716],[427,714],[622,729]]
            #if entry == 2004: portals = [[-698,181],[-696,206],[-695,262],[-695,334],[-695,262],[-696,333],[-697,385],[-612,714],[-579,715],[-487,716],[-362,708],[233,713],[-98,717],[40,716],[161,718]]

            if entry == 2001: portals = [[-86,-559],[76,-560], [143,-559], [171,-558], [194,-560], [273,-560], [427,-559], [598,-562], [861,-515], [866,-468], [862,-198]]
            if entry == 2002: portals = [[-199,-560], [-219,-560], [-356,-560], [-617,-563], [-631,-558], [-927,-514], [-882,-513]]
            if entry == 2003: portals = [[864,130], [864,165], [868,387], [868,473], [867,786], [866,820], [866,874], [837,1084], [778,1093], [605,1085], [582,1091], [482,1085], [421,1086], [338,1087], [308,1086], [141,1083], [111,1087], [89,1086]]
            if entry == 2004: portals = [[-1016,801], [-1031,918], [-1028,1080], [-848,1084], [-728,1104], [-585,1086], [-440,1085], [-347,1076], [-231,1090], [-150,1085], [-44,1094]]

            portal = random.choice(portals)
            r = Pedestrian.Pedestrian()
            r.set_location(portal[0],portal[1])
            #r.set_location(locdict[entry][0],locdict[entry][1])
            #r.set_random_location()
            r.destweights = od
            r.origins = origins
            hotspot, goal = pick_first(origins)
            r.hotspot = hotspot
            r.set_goal(goal)
            r.set_path()
            pedestrians.append(r)
        #print 'supposed to be: ',number_of_agents
        #print 'there is: ',len(pedestrians)
        for p in pedestrians:
            #pth = []
            #for f in p.path:
            #    px = f[0]*ZOOM+ORIGINX
            #    py = f[1]*ZOOM+ORIGINY
            #    pth.append([px,py])
            #pygame.draw.lines(screen, (0, 255, 0), False, pth, 2)
            p.update()
            if p.routenodes != None:
                #print p.routenodes
                for r in p.routenodes:
                    #trail = xynodes[r]
                    nodevisual[r]+=1
                p.routenodes = None
                    #hmark = []
                    #for i in trail:
                        #hmark.append([int(i[0])*ZOOM+ORIGINX,int(i[1])*ZOOM+ORIGINY])
                    #pygame.draw.polygon(screen, (255,255,255),hmark, 1)
                    #n = check_node(r)
                    #nodevisual[n]+=1
                    #pygame.draw.polygon(screen, (255, 255, 50), (int(r[0])*ZOOM+ORIGINX, int(r[1])*ZOOM+ORIGINY), 2)
            #heatpoint = p.node
            #if heatpoint != None:
                #hcoord = xynodes[heatpoint]
                #hmark = []
                #for i in hcoord:
                    #hmark.append([int(i[0])*ZOOM+ORIGINX,int(i[1])*ZOOM+ORIGINY])
                #pygame.draw.polygon(screen, (255,255,255),hmark, 1)
            #obs = p.define_observation()
            #observation = []
            #for o in obs:
                #ox = o[0]*ZOOM+ORIGINX
                #oy = o[1]*ZOOM+ORIGINY
                #observation.append([ox,oy])            
            #pygame.draw.polygon(screen, (0,255,0), observation, 1)
            #PEDESTRIAN DRAWING HAPPENS HERE
            #if p.exiting == False: pygame.draw.circle(screen, (50, 255, 50), (int(p.x)*ZOOM+ORIGINX, int(p.y)*ZOOM+ORIGINY), 2)
            #else: pygame.draw.circle(screen, (255, 100, 50), (int(p.x)*ZOOM+ORIGINX, int(p.y)*ZOOM+ORIGINY), 2)

            #pygame.draw.circle(screen, (50, 255, 50), (int(p.x)*ZOOM+ORIGINX, int(p.y)*ZOOM+ORIGINY), 2)
            #print "Wat happens",p.x,p.y
        frame = 0
        #print nodevisual
        pygame.display.flip()
    if pygame.font:
        font = pygame.font.Font(None, 36)
        timetext = font.render(str(day),0,(0,255,10))
        hourtext = font.render(hour+':00',0,(0,255,10))
        text = font.render(str((xpos,ypos)), 1, (0, 255, 10))
        textpos = text.get_rect(centerx=screen.get_width()-100)
        timepos = text.get_rect(centerx=screen.get_width()-300)
        hourpos = text.get_rect(centerx=screen.get_width()-150)
        screen.fill(black)
        #screen.fill(black, textpos)
        #screen.fill(black, hourpos)
        screen.blit(text, textpos)
        #screen.fill(black, timepos)
        screen.blit(timetext, timepos)                              
        screen.blit(hourtext, hourpos)
        pygame.display.update(textpos)
        pygame.display.update(timepos)    
        pygame.display.update(hourpos)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        if BTCAPTURE == True:
            for key,value in nodevisual.iteritems():
                btwriter.writerow([key,value])
        if RANDOMCAPTURE == True:
            for key,value in nodevisual.iteritems():
                rwriter.writerow([key,value])
        running = 0
    if event.type == KEYDOWN and event.key == K_q:
        global ZOOM
        ZOOM = ZOOM + 1
        print 'ZOOM',ZOOM
    if event.type == KEYDOWN and event.key == K_a:
        global ZOOM
        ZOOM = ZOOM - 1
        if ZOOM == 0: ZOOM = 1
        print 'ZOOM',ZOOM
    if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.mouse.get_rel()
        print event.button
    if event.type == pygame.MOUSEBUTTONUP:
        global ORIGINX
        global ORIGINY
        mousepos = pygame.mouse.get_rel()
        ORIGINX = ORIGINX + mousepos[0] 
        ORIGINY = ORIGINY + mousepos[1]
        #print mousepos
    
    # if event.type == pygame.MOUSEBUTTONDOWN:
    #     pedestrian_simulation = False
    #     screen.fill(black)
    #     draw_map()
    #     if pedestrian_simulation == False: draw_gps(mode)
    #     #draw_route()
    #     mode = mode+1
    #     if mode == 7:
    #         pedestrian_simulation = True
    #         print "Simulating pedestrians", pedestrian_simulation
    #     if mode == 8: mode = 0
    #     pygame.display.flip()

