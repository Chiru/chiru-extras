###############################################################################################################################
#DISCLAIMER:
#Use at your own risk! Under no circumstances  shall the author(s) or contributor(s) be liable for damages resulting directly #
#or indirectly from the use or non-use of this code.                                                                          #
###############################################################################################################################
from math import sqrt
import itertools
import csv

#This OBJ loader is probably from http://www.nandnor.net/?p=86. Changed it a little bit (For example, there are no normals specified in the
#OBJ navmesh exported) 
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

def euclidean(a,b):
    distance = sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2 + (b[2] - a[2])**2)
    return distance

def approx_Equal(x, y, tolerance=0.00001):
    for a,b in zip(x,y):
        test = abs(a-b) <= 0.5 * tolerance * (a + b)
        if test == False:
            return False
    return True

def group(lst, n):
    return zip(*[lst[i::n] for i in range(n)])

vertlist = loadOBJ("largenav2.obj")

nodes = group(vertlist,3)
xynodes = []

#print nodes

for i in nodes:
    newnode=[]
    for v in i:
        xyvertex=[]
        xyvertex.append(v[0])
        xyvertex.append(v[2])
        newnode.append(xyvertex)
    xynodes.append(newnode)

def findCentroid(v1,v2,v3):
    x = (v1[0]+v2[0]+v3[0])/3
    #y = (v1[1]+v2[1]+v3[1])/3
    z = (v1[2]+v2[2]+v3[2])/3
    return(x,z)

def findCentroid2D(v1,v2,v3):
    x = (v1[0]+v2[0]+v3[0])/3
    y = (v1[1]+v2[1]+v3[1])/3
    #z = (v1[2]+v2[2]+v3[2])/3
    return(x,y)

def findNeighbors(node):
    v1 = node[0]
    v2 = node[1]
    v3 = node[2]
    #print "vertex 1: ",v1," vertex2: ",v2," vertex3: ", v3
    commonvertices=0
    neighbors=[]
    for i in nodes:
        commonvertices=0
        for a,b in itertools.product(node, i):
            distance = euclidean(a,b)
            if distance<0.00001:
                commonvertices=commonvertices+1
        if commonvertices == 2:
            #print "Found 2"
            neighbors.append(nodes.index(i))                      
    return neighbors

#def findNeighbors2(node):
#    v1 = node[0]
#    v2 = node[1]
#    v3 = node[2]
    #print "vertex 1: ",v1," vertex2: ",v2," vertex3: ", v3
#    commonvertices=0
#    neighbors=[]
#    for i in nodes:
#        commonvertices=0
#        for a,b in itertools.product(node, i):
#            if approx_Equal(a,b):
#                commonvertices=commonvertices+1
#        if commonvertices == 2:
            #print "Found 2"
#            neighbors.append(nodes.index(i))                      
#    return neighbors


def create_nodes():
    nodeinfo={}
    coords=[]
    neighbors=[]
    for n in nodes:
        nb = findNeighbors(n)
        c = findCentroid(n[0],n[1],n[2])
        #print 'Node: ', nodes.index(n), ' Centroid: ',c, ' Neighbours: ',nb
        #nodeinfo[nodes.index(n)]=(c,nb)
        coords.append(c)
        neighbors.append(nb)
    return coords,neighbors
crd,neigb = create_nodes()

import csv
with open('graph5.csv', 'wb') as csvfile:
    graphwriter = csv.writer(csvfile, delimiter=',')
    for f,g in zip(crd,neigb):
        graphwriter.writerow([f,g])

with open('nodes5.csv', 'wb') as csvnode:
    nodewriter = csv.writer(csvnode, delimiter=',')
    for n in xynodes:
        nodewriter.writerow(n)

nbcent = []

#I think I found this from http://www.ariel.com.au/a/python-point-int-poly.html
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


#startx = 86.62783266666668
#starty = 37.055328
startx = 48.0 #You can change these coordinates to test finding the nodes 
starty = -132.0
endx = -120.0
endy = 131.0

def find_node(x,y):
    for n in xynodes:
        if point_inside_polygon(x,y,n):
            print 'Found node'
            return xynodes.index(n)

startnode = find_node(startx,starty)
endnode = find_node(endx,endy)

print 'Start node: ', startnode
print 'End node: ', endnode    


