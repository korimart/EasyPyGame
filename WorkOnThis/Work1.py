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

def sanitiyCheck(locations, map):
        lst = []
        for p in locations:
            if map.getTerrain(p == 0):
                lst.append(p)
        return lst
    
def calculateCoordinates(coord, direction):
    newCoord = list(coord)
    if direction == 0:
        newCoord[1] += 1 
    elif direction == 1:
        newCoord[0] += 1
    elif direction == 2:
        newCoord[1] -= 1
    elif direction == 3:
        newCoord[0] -= 1
    return tuple(newCoord)

def possiblePositions(curPos, map):
    positions = list()
    for dir in range(4):
        positions.append(calculateCoordinates(curPos, dir))
    return sanitiyCheck(positions, map)

def ManhattanDistance2D(x1, x2):
        d = 0
        d += abs(x1[0] - x2[0])
        d += abs(x1[1] - x2[1])
        return d

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

        visited = set()
        queue.push([pointA])
        visited.add(pointA)
        while(len(queue) != 0):
            # paint()
            path = queue.pop()
            current = path[-1]
            if pointB == current:
                return path
            possiblePos = possiblePositions(current, map)
            for position in possiblePos:
                if position not in visited:
                    visited.add(position)
                    copiedPath = path.copy()
                    copiedPath.append(position)
                    queue.append(copiedPath)
        return None

class IDAstar:
    def __init__(self, dsFactory):
        self.dsFactory = dsFactory

    def findPath(self, pointA, pointB, map):
        stack = self.dsFactory("stack")
        bound = ManhattanDistance2D(pointA, pointB)
        stack.append(pointA)
        while True:
            t = self.IDA_star_search(pointB, stack, 0, bound, map)
            if t == "Found":
                return stack
            if t == -1:
                return None
            bound = t

    def IDA_star_search(self, end, path, g, bound, map):
        node = path[-1]
        f = g + ManhattanDistance2D(node, end)
        if f > bound:
            return f
        if end == node:
            return "Found"
        min = None
        for next in possiblePositions(node, map):
            if next not in path:
                path.append(next)
                t = self.IDA_star_search(end, path, g + 1, bound, map)
                if t == "Found":
                    return "Found"
                if t != None:
                    if min == None:
                        min = t
                    elif t < min:
                        min = t                   
                path.pop(-1)
        return min
