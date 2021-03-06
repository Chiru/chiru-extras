import mesh_grid5
#from mapvisualsteer import string_pull, vdistsqr
from mapvisual5 import string_pull, vdistsqr, pick_first, pick_second, find_closest
from model import pick_with_type, weighted_choice, find_n_closest_w_distance
from math import sin, cos, atan2, degrees, radians, sqrt
from random import randint, choice
#import od
#import pdb

def subtract(l1,l2):
    answer = []
    for x,y in zip(l1,l2):
        answer.append(x-y)
    return answer

def multiply_with_scalar(l1,s):
    answer = []
    for x in l1:
        answer.append(x*s)
    return answer

def normalize_vector(v):
    magnitude = sqrt(v[0]**2+v[1]**2)
    if magnitude == 0: return v
    uv = [v[0]/magnitude,v[1]/magnitude]
    return uv

def dot(v1,v2):
    answer = 0
    for a,b in zip(v1,v2):
        answer = answer + a*b
    return answer

class Pedestrian(object):
    def __init__(self):
        self.node = None
        self.goal = None
        self.id = 0
        self.x = 0
        self.y = 0
        self.speed = 0
        self.heading = [0,0]
        self.velocity = [0,0]
        self.relative_move_force = []
        self.mass = 10
        self.max_force = 10
        self.max_speed = 2
        self.safedistance = 3
        self.observationdistance = 10
        self.orientation = 0
        self.target_id = None
        self.path = []
        self.routenodes = None
        self.destnumber = None
        self.lost = False
        self.neighbors = []
        self.close_neighbors = []
        self.hotspot = None
        self.destweights = None
        self.origins = None
        self.exiting = False
        self.to_be_destroyed = False
        self.aorigins = []

    def set_random_location(self):
        location = mesh_grid5.random_target()
        self.node = location
        self.x = mesh_grid5.coords[location][0]
        self.y = mesh_grid5.coords[location][1]

    def set_location(self,x,y):
        self.x = x
        self.y = y

    def set_random_goal(self):
        #Fiksaa jos tulee paikka johon ei paase
        self.goal = mesh_grid5.random_target()

    def set_goal_by_coordinates(self,goal):
        self.goal = mesh_grid5.find_node(goal[0],goal[1])

    def set_goal(self,goal):
        #print goal
        self.goal = goal
        
    def set_path(self):
        location = mesh_grid5.find_node(self.x,self.y)
        if location == None: location = find_closest([self.x,self.y])
        # Jos joutuu tyhjalle niin nakojaan osaa itse kavella lahimpaan
        #print "Location: ",location
        route = mesh_grid5.search_path(location,self.goal)
        if route == None:
            #pdb.set_trace() 
            #print "No route, what happens?"
            self.destnumber = 0
            return None
        self.routenodes = [r[1] for r in route]
        edges = mesh_grid5.search_portals(location,self.goal)
        self.path = string_pull([r[0] for r in route],edges)
        self.destnumber = 0

    def get_position(self):
        return self.x,self.y

    def get_closest_exit(self,hotspot):
        pos = self.get_position()
        exits = []
        distances = []
        #if hotspot == 2001: exits = [[-36,-192],[35,-138],[131,-78],[235,-5]]
        #if hotspot == 2003: exits = [[235,-5],[178,68],[122,154],[59,244]]
        #if hotspot == 2004: exits = [[59,244],[-38,182],[-121,125],[-211,67]]
        #if hotspot == 2002: exits = [[-211,67],[-149,-26],[-97,-112],[-44,-192]]
        #if hotspot == 2001: exits = [[75,-560],[144,-560],[172,-560],[195,-561],[274,-559],[427,-558],[598,-560],[680,-460],[679,-429],[678,-392],[681,-232],[675,-160],[675,-106]] 
        #if hotspot == 2002: exits = [[-617,-561],[-218,-554],[-199,559],[-86,-560],[-356,-560],[-698,-474],[-696,-376]]
        #if hotspot == 2003: exits = [[681,26],[676,271],[677,384],[676,440],[264,713],[386,716],[427,716],[427,714],[622,729]]
        #if hotspot == 2004: exits = [[-698,181],[-696,206],[-695,262],[-695,334],[-695,262],[-696,333],[-697,385],[-612,714],[-579,715],[-487,716],[-362,708],[233,713],[-98,717],[40,716],[161,718]]

        if hotspot == 2001: exits = [[-86,-559],[76,-560], [143,-559], [173,-560], [195,-554], [273,-560], [427,-559], [598,-562], [861,-515], [866,-468], [862,-198]]
        if hotspot == 2002: exits = [[-199,-560], [-219,-560], [-356,-560], [-617,-563], [-631,-558], [-927,-514], [-882,-513]]
        if hotspot == 2003: exits = [[864,130], [864,165], [868,387], [868,473], [867,786], [866,820], [866,874], [837,1084], [778,1093], [605,1085], [582,1091], [482,1085], [421,1086], [338,1087], [308,1086], [141,1083], [111,1087], [89,1086]]
        if hotspot == 2004: exits = [[-1016,801], [-1031,918], [-1028,1080], [-848,1084], [-728,1104], [-585,1086], [-440,1085], [-347,1076], [-231,1090], [-150,1085], [-44,1094]]


        for r in range(len(exits)):
            distances.append([vdistsqr(pos,exits[r]),r])
        #print 'not sorted: ',distances
        distances.sort()
        self.set_goal_by_coordinates(exits[distances[0][1]])
        #self.set_goal_by_coordinates([195,-554])
        #print exits[distances[0][1]]
        #print 'sorted: ',distances

    def update(self):
        if len(self.path) > 0 and self.path != None:
            if self.destnumber == len(self.path):
                if self.exiting == True: 
                    self.to_be_destroyed = True
                    return
                del self.path[:]
                #print self.hotspot
                #print self.destweights
                AHS_MODE = False
                if AHS_MODE == True:
                    raffle = randint(1,10) #Picking random walkers to exit
                    if raffle == 10:
                        self.exiting = True
                        passage = choice([2001,2002,2003,2004])
                        self.get_closest_exit(passage) 
                        self.set_path()
                    if raffle == 9: 
                        self.set_random_goal()
                        self.set_path()
                    else:
                        print 'ped aorigins',self.aorigins 
                        atype = weighted_choice(self.aorigins)
                        #print atype
                        ahs = pick_with_type(atype)
                        print ahs
                        goals = find_n_closest_w_distance(ahs,150,atype)
                        #print goals
                        goal = choice(goals)
                        #print goal
                        self.set_goal(goal)
                        self.set_path()
                    return
                RANDOM_MODE = True
                if RANDOM_MODE == False:
                    if self.destweights[self.hotspot]==[]: 
                        hs,gl = pick_first(self.origins) 
                    else: hs, gl = pick_second(self.hotspot, self.destweights) 
                    #print 'going random'
                    if hs == 2001 or hs == 2002 or hs == 2003 or hs == 2004: 
                        self.exiting = True 
                        self.get_closest_exit(hs) 
                        self.set_path()
                        return 
                        #print 'Im exiting'
                    self.hotspot = hs
                    self.set_goal(gl) 
                else:
                    raffle = randint(1,10) #Picking random walkers to exit
                    if raffle == 10:
                        self.exiting = True
                        passage = choice([2001,2002,2003,2004])
                        self.get_closest_exit(passage) 
                    else: self.set_random_goal()
                self.set_path()
                if len(self.path) == 0:
                    return
            self.speed = 6
            #self.get_close_neighbors()
            if len(self.close_neighbors) >0:
                changeforce = self.velocity_change()
                changenorm = normalize_vector(changeforce)
                #change = multiply_with_scalar(changenorm,self.speed)
                change = multiply_with_scalar(changenorm,1.5)
                self.x = self.x+((self.velocity[0]+changenorm[0])/2)
                self.y = self.y+((self.velocity[1]+changenorm[1])/2)
                loc = [self.x,self.y]
                self.velocity = change
                #print change
                #print "Got neighbors"
                return




            current_destination = self.path[self.destnumber]
            dy = self.y-float(current_destination[1])
            dx = self.x-float(current_destination[0])
            dx = dx*-1
            dy = dy*-1
            angle = atan2(dy,dx)
            angle = degrees(angle)
            self.rotation = angle
            self.heading = [cos(angle),sin(angle)]
            vector_to_goal = [dx,dy]
            distance_to_goal = sqrt((dx**2)+(dy**2))
            if distance_to_goal > 0:
                direction = [dx/distance_to_goal,dy/distance_to_goal]
            else: direction = vector_to_goal
            new_velocity = multiply_with_scalar(self.heading,self.speed)
            self.x = self.x+((self.velocity[0]+direction[0])/2)
            self.y = self.y+((self.velocity[1]+direction[1])/2)
            self.velocity = direction
            loc = [self.x,self.y]
            #location = mesh_grid5.find_node(self.x,self.y)
            #self.node = location
            #print vdistsqr(loc,current_destination) 
            if vdistsqr(loc,current_destination) < 0.5:
                #print self.destnumber
                self.destnumber = self.destnumber +1
            #self.draw()

        else:
            self.set_random_goal()
            self.set_path()
            #print "Checking again"
            if self.path == None: print "waaat"

    def define_observation(self):
        l = 12
        w = 7
        x1 = self.x
        y1 = self.y
        #dvector = multiply_with_scalar(self.heading,w)
        dturned = [(self.velocity[1]*-1),self.velocity[0]]
        p1x = x1 - dturned[0] * w / 2
        p1y = y1 - dturned[1] * w / 2
        p2x = p1x + dturned[0] * w 
        p2y = p1y + dturned[1] * w
        p3x = p2x + self.velocity[0] * l
        p3y = p2y + self.velocity[1] * l
        p4x = p1x + self.velocity[0] * l
        p4y = p1y + self.velocity[1] * l

        return [[p1x,p1y],[p2x,p2y],[p3x,p3y],[p4x,p4y]]
        
    def get_close_neighbors(self):
        close_neighbors = []
        obs = self.define_observation()
        for p in self.neighbors:
            if mesh_grid5.point_inside_polygon(p.x,p.y,obs):
                #close_neighbors.append([p.x,p.y])
                close_neighbors.append(p)
        self.close_neighbors = close_neighbors
        #return neighbors

    def velocity_change(self):
        current_destination = self.path[self.destnumber]
        dy = self.y-float(current_destination[1])
        dx = self.x-float(current_destination[0])
        dx = dx*-1
        dy = dy*-1
        distance_to_goal = sqrt((dx**2)+(dy**2))
        if distance_to_goal > 0:
            preferred_velocity = [dx/distance_to_goal,dy/distance_to_goal]
        else: preferred_velocity = [dx,dy]
        #preferred_velocity = multiply_with_scalar(preferred_velocity,-1) #whaaat
        repulsion = self.get_repulsion_force()
        #velocity_change = [preferred_velocity[0]+repulsion[0],preferred_velocity[1]+repulsion[1]]
        velocity_change = [self.velocity[0]+preferred_velocity[0]+repulsion[0],self.velocity[1]+preferred_velocity[1]+repulsion[1]]
        return velocity_change
        #return preferred_velocity
        #return self.velocity
        #return repulsion

    def get_repulsion_force(self):
        force = [0,0]
        for j in self.close_neighbors:
            vi = self.velocity
            if self.velocity == [0,0]:
                return force
            vj = j.velocity
            #dji = [j.x-self.x,j.y-self.y]
            dji = [self.x-j.x,self.y-j.y]
            dw = 7
            dl = 12
            vinorm = normalize_vector(vi)
            if dji > 0: 
                djinorm = normalize_vector(dji)
            else: djinorm = dji 
            djivi = [djinorm[0]+vinorm[0],djinorm[1]+vinorm[1]]
            djivimagn = sqrt(djivi[0]**2+djivi[1]**2)
            tj = [djivi[0]/djivimagn,djivi[1]/djivimagn]
            distanceij = sqrt((j.x-self.x)**2+(j.y-self.y)**2)
            wdi = (dl - distanceij)/dl
            minusvj = multiply_with_scalar(vj,-1)
            woi = dot(vi,minusvj)/2+1.5
            Fobji = multiply_with_scalar(tj,wdi*woi)
            force = [force[0]+Fobji[0],force[1]+Fobji[1]]
        return force
            

    def get_relative_position(self, other):
        return [self.x-other.x,self.y-other.y]

    def get_relative_velocity(self, other):
        return subtract(self.velocity,other.velocity)

