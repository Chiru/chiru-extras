from astar_meshgrid import AStarGrid, AStarGridNode
from itertools import product, tee, izip
from math import sqrt
#from sets import Set
#import meshreader
import csv
import random
#graphreader = csv.reader(open('pyplugins/grapht.csv', 'rb'), delimiter=',')
#nodereader = csv.reader(open('pyplugins/nodest.csv', 'rb'), delimiter=',')
graphreader = csv.reader(open('graph5.csv', 'rb'), delimiter=',')
nodereader = csv.reader(open('nodes5.csv', 'rb'), delimiter=',')

#coords,neighbors = meshreader.create_nodes()

coords = []
neighbors = []
triangles = []

for row in graphreader:
    c = row[0]
    n = row[1]
    c = tuple(map(float, c[1:-1].split(',')))
    #print c
    if len(n)>0:
        n = tuple(map(int, n[1:-1].split(',')))
    #print n
    #c = (int(x) for x in c.split(","))
    coords.append(c)
    neighbors.append(n)

for row in nodereader:
    x = row[0]
    y = row[1]
    z = row[2]
    x = tuple(map(float, x[1:-1].split(',')))
    y = tuple(map(float, y[1:-1].split(',')))
    z = tuple(map(float, z[1:-1].split(',')))
    triangles.append([x,y,z])
    #triangles.append(row)

#triangleset = Set()
#for t in triangles:
    #triangleset.add(tuple(t))

def euclidean(a,b):
    distance = sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
    #print distance
    return distance

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def check_edge(n1,n2):
    edge = []
    for a,b in product(n1, n2):
        distance = euclidean(a,b)
        if distance<0.00001:
             edge.append(a)
    if len(edge)==2:
        return edge
    return None

def make_graph():
    nodes = []
    #for f in coords:
    #    x = f[0]
    #    y = f[1]
    #    nodes.append(AstarGridNode(x,y))     
    #nodes = [AStarGridNode(x, y, v1, v2, v3) for x, y in coords for v1,v2,v3 in triangles]
    #nodes = [AStarGridNode(x, y) for x, y in coords]
    for a,b in zip(coords,triangles):
        x,y = a[0],a[1]
        v1,v2,v3 = b[0],b[1],b[2]
        nodes.append(AStarGridNode(x,y,v1,v2,v3))
    #for f in nodes:
    #    print f.x
    #    print f.y
    #b = raw_input('Press enter to continue')
    graph = {}
    #for x, y in product(range(mapinfo.width), range(mapinfo.height)):
    #    node = nodes[x][y]
    #    graph[node] = []
    for z,y in zip(nodes, neighbors):
        graph[z] = []
        #nb=[]
        if len(y)>0:
            for i in y:
                #nb.append(AStarGridNode(i[0],i[1]))
                #graph[z].append(AStarGridNode(i[0],i[1]))
                graph[z].append(nodes[i])
        #graph[z].append(nb)        
    return graph, nodes

graph, nodes = make_graph()
paths = AStarGrid(graph)
#start, end = nodes[56], nodes[296]


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

def find_node(x,y):
    for n in range(len(triangles)):
        #test = pnpoly(x,y,triangles[n])
        #if test == True:
        if point_inside_polygon(x,y,triangles[n]):
            #print 'Found node'
            #return triangles.index(list(n))
            return n

def random_target():
    target = random.randint(0, len(nodes)-1)
    return target    

def search_path(a,b):
    route = []
    edges = []
    start, end = nodes[a], nodes[b]
    #print "***** Search starts now"
    path = paths.search(start, end)
    if path is None:
        #print "No path found"
        return None
    else:
        #print "Path found:"
        for ob in path:
            #print nodes.index(ob) 
            #print ob
            #print ob.x,ob.y
            route.append([[ob.x,ob.y],nodes.index(ob)])
            
        for i,j in pairwise(path):
            n1 = [i.v1,i.v2,i.v3]
            n2 = [j.v1,j.v2,j.v3]
            edge = check_edge(n1,n2)
            edges.append(edge)
        return route

def search_portals(a,b):
    route = []
    edges = []
    start, end = nodes[a], nodes[b]
    #print "***** Search starts now"
    path = paths.search(start, end)
    if path is None:
        print "No path found"
        return None
    else:
        #print "Path found:"
           
        for i,j in pairwise(path):
            n1 = [i.v1,i.v2,i.v3]
            n2 = [j.v1,j.v2,j.v3]
            edge = check_edge(n1,n2)
            edges.append(edge)
        return edges


#testi = find_node(5,-92)
#print testi
#import timeit

#edgelist = search_portals(119,random_target())
#for i in edgelist:
#    print "first: ",i[0],"second: ",i[1]

#t = timeit.Timer(stmt="search_path(119,random_target())", setup="from __main__ import search_path,random_target") 
#print t.timeit(number=1000)
#for r in range(100):
#    b = 231
#    a = random_target()
#    route = search_path(a,b)
#    print route

