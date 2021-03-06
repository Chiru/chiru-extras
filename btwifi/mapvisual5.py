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

w = 1152                 #set width of screen
#h = 864                 #set height
h = 1000
screen = pygame.display.set_mode((w, h)) #make screen
pygame.font.init()
running = 1
global ORIGINX, ORIGINY
global ZOOM
ZOOM = 2
ORIGINX = screen.get_width()/2 #move origin 
ORIGINY = (screen.get_height()-100)/2 #move origin
black = 0, 0, 0
colorscheme = [[255, 255, 217],[237, 248, 217],[199, 233, 180],[127, 205, 187],[65, 182, 196],[29, 145, 192],[34, 94, 168],[37, 52, 148],[8, 29, 88]]
#colorscheme = [[255, 255, 204],[255, 237, 160],[254, 217, 118],[254, 178, 76],[253, 141, 60],[252, 78, 42],[227, 26, 28],[189, 0, 38],[128, 0, 38]]
colorscheme.reverse()
#black = 255, 255, 255 #If you want a white background
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

vertlist = loadOBJ("largenav2.obj")

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

def draw_map():
    for n in xynodes:
        intnode = []
        for i in n:
            intnode.append([int(i[0])*2+ORIGINX,int(i[1])*2+ORIGINY])
        #print intnode
        #pygame.draw.circle(screen, (0, 255, 0), (int(n[0]), int(n[1])), 1)
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
    pygame.draw.circle(screen, (255, 0, 0), (int(acoord[0])*2+ORIGINX, int(acoord[1])*2+ORIGINY), 4)
    pygame.draw.circle(screen, (0, 255, 100), (int(bcoord[0])*2+ORIGINX, int(bcoord[1])*2+ORIGINY), 4)
    pygame.draw.circle(screen, (255, 255, 255), (int(sm[0])*2+ORIGINX, int(sm[1])*2+ORIGINY), 4)
    pygame.draw.circle(screen, (255, 255, 255), (int(nuclear[0])*2+ORIGINX, int(nuclear[1])*2+ORIGINY), 4)
    route = mesh_grid5.search_path(a,b)
    edges = mesh_grid5.search_portals(a,b)
    pygame.display.flip()
    if route:
        path = []
        funnelpoints = string_pull(route,edges)
        #print funnelpoints
        for f in funnelpoints:
            px = f[0]*2+ORIGINX
            py = f[1]*2+ORIGINY
            path.append([px,py])
        pygame.draw.lines(screen, (0, 255, 0), False, path, 2)
        for f in funnelpoints:
            pygame.draw.circle(screen, (0, 255, 100), (int(f[0])*2+ORIGINX, int(f[1])*2+ORIGINY), 4)
           
        #for r in route:
            #pygame.draw.circle(screen, (0, 255, 100), (int(r[0])*2+ORIGINX, int(r[1])*2+ORIGINY), 3)
    if tlist:
        for t in tlist:
            if not check_node(t):
                b = [0,0]
                b[0], b[1] = t[1], t[0]
                #print "What happens: ",t
                c = mesh_grid5.coords[find_closest(b)]
                pygame.draw.circle(screen, (255, 255, 255), (int(c[0])*2+ORIGINX, int(c[1])*2+ORIGINY), 3)
                pygame.draw.circle(screen, (100, 100, 100), (int(t[0])*2+ORIGINX, int(t[1])*2+ORIGINY), 3)
            #print "wat"
            #print t[0],t[1]
            else:
                pygame.draw.circle(screen, (50, 255, 50), (int(t[0])*2+ORIGINX, int(t[1])*2+ORIGINY), 3)
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

            pygame.draw.circle(screen, (255, 255, 255), (int(left[0])*2+ORIGINX, int(left[1])*2+ORIGINY), 2)
            pygame.draw.circle(screen, (100, 100, 255), (int(right[0])*2+ORIGINX, int(right[1])*2+ORIGINY), 2)     
            #pygame.draw.circle(screen, (255, 255, 255), (int(e[0][0])*2+ORIGINX, int(e[0][1])*2+ORIGINY), 2)
            #pygame.draw.circle(screen, (100, 100, 255), (int(e[1][0])*2+ORIGINX, int(e[1][1])*2+ORIGINY), 2)
            #pygame.draw.line(screen, (255,255,255), (int(e[0][0])*2+ORIGINX, int(e[0][1])*2+ORIGINY), (int(e[1][0])*2+ORIGINX, int(e[1][1])*2+ORIGINY), 2)

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

starttime = time.time()
odmatrix = odcontainer.OriginContainer()
if __name__ == "__main__":
    day = '2012-05-05'
    #dstmp = time.strptime(day,"%Y-%m-%d")
    #print dstmp
    hour = '0'
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
while running and __name__ == "__main__":
    global mode
    global pedestrian_simulation
    elapsed_time = time.time() - starttime
    #print elapsed_time
    if elapsed_time > 10: #You can set the speed of time changes here
        starttime = time.time()
        day,hour = update_time(day,int(hour))
        odmatrix.update_weights(day,hour)
        origins = odmatrix.get_origins()
        #print origins
        od = odmatrix.get_od()
        number_of_agents = odmatrix.get_pedno()
        for ped in pedestrians:
            ped.destweights = od
            ped.origins = origins
        #print pedestrians[0].destweights
    #Set true if want animated pedestrians
    mpos = pygame.mouse.get_pos()
    xpos = (mpos[0]-ORIGINX)/2
    ypos = (mpos[1]-ORIGINY)/2
    frame = frame +1
    if frame == 20 and pedestrian_simulation == True:
        #screen.fill(black)
        #print "Simulating..."
        #mode = 3
        #screen.fill(black)
        draw_map()
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
            pygame.draw.circle(screen, (colorscheme[intensity][0],colorscheme[intensity][1],colorscheme[intensity][2]),(int(x*2+ORIGINX), int(y*2+ORIGINY)), 5)
            #pygame.draw.circle(screen, (int(intensity),0,255-intensity), (int(x*2+ORIGINX), int(y*2+ORIGINY)), 5)
        pedestrians = [p for p in pedestrians if p.to_be_destroyed == False]
        if len(pedestrians) < number_of_agents:
            #print 'oeoe'
            entrys = []
            #print origins
            for key in origins:
                if key == 2001 or key == 2002 or key == 2003 or key == 2004: entrys.append([key,origins[key]])
            entry = weighted_choice(entrys)
            if entry == 2001: portals = [[-36,-192],[35,-138],[131,-78],[235,-5]]
            if entry == 2003: portals = [[235,-5],[178,68],[122,154],[59,244]]
            if entry == 2004: portals = [[59,244],[-38,182],[-121,125],[-211,67]]
            if entry == 2002: portals = [[-211,67],[-149,-26],[-97,-112],[-44,-192]]
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
            #    px = f[0]*2+ORIGINX
            #    py = f[1]*2+ORIGINY
            #    pth.append([px,py])
            #pygame.draw.lines(screen, (0, 255, 0), False, pth, 2)
            p.update()
            #obs = p.define_observation()
            #observation = []
            #for o in obs:
                #ox = o[0]*2+ORIGINX
                #oy = o[1]*2+ORIGINY
                #observation.append([ox,oy])            
            #pygame.draw.polygon(screen, (0,255,0), observation, 1)
            pygame.draw.circle(screen, (50, 255, 50), (int(p.x)*2+ORIGINX, int(p.y)*2+ORIGINY), 2)
            #print "Wat happens",p.x,p.y
        frame = 0
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
		running = 0
    if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.mouse.get_rel()
    if event.type == pygame.MOUSEBUTTONUP:
        global ORIGINX
        global ORIGINY
        mousepos = pygame.mouse.get_rel()
        ORIGINX = ORIGINX + mousepos[0] 
        ORIGINY = ORIGINY + mousepos[1]
        print mousepos
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

