# REFERENCES (use the following)
#
# DSFactory class methods:
#
#   dsFactory.get(type) -> returns a data structure
#       type is either "queue", "stack", "graph"
#  
# Queue class methods:
# 
#   queue.push(item)
#   queue.pop()
#
# Stack class methods:
#
#   stack.push(item)
#   stack.pop()
#
# Map class methods:
#
#   map.getTerrain(x, y) -> returns 0 (nothing) or 1 (hazard)
#       out-of-scope values also return 1

class Terrain:
    NOTHING = 0
    HAZARD = 1

class BFS:
    def __init__(self, dsFactory):
        self.dsFactory = dsFactory

    def findPath(self, pointA, pointB, map):
        # implement this
        # pointA and pointB are tuples of length 2
        # return a list of points on the calculated path
        queue = self.dsFactory("queue")
        pass

class AStar:
    def __init__(self, dsFactory):
        self.dsFactory = dsFactory

    def findPath(self, pointA, pointB, map):
        # implement this
        pass