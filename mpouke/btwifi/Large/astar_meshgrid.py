from astar import AStar, AStarNode
from math import sqrt

class AStarGrid(AStar):
    def heuristic(self, node, start, end):
        return sqrt((end.x - node.x)**2 + (end.y - node.y)**2)

class AStarGridNode(AStarNode):
    def __init__(self, x, y, v1, v2, v3):
    #def __init__(self, x, y):    
        self.x, self.y = x, y
        self.v1, self.v2, self.v3 = v1, v2, v3
        super(AStarGridNode, self).__init__()

    def move_cost(self, other):
        #diagonal = abs(self.x - other.x) == 1 and abs(self.y - other.y) == 1
        #return 14 if diagonal else 10
        #print other
        cost = sqrt((other.x - self.x)**2 + (other.y - self.y)**2)
        #cost = sqrt((other[0] - self.x)**2 + (other[1] - self.y)**2)
        return cost
