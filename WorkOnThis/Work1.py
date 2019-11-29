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
#   queue.len()
#
# Stack class methods:
#
#   stack.push(item)
#   stack.pop()
#   stack.peek()
#   stack.getList()
#   

# Map class methods:
#
#   map.getTerrain(x, y) -> returns 0 (nothing) or 1 (hazard)
#       out-of-scope values also return 1

def sanitiyCheck(locations, mmap):
        lst = []
        for p in locations:
            if mmap.getTerrain(p[0], p[1]) == 0:
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

def possiblePositions(curPos, mmap):
    positions = list()
    for direc in range(4):
        positions.append(calculateCoordinates(curPos, direc))
    return sanitiyCheck(positions, mmap)

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

    def findPath(self, pointA, pointB, mmap):
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
            possiblePos = possiblePositions(current, mmap)
            for position in possiblePos:
                if position not in visited:
                    visited.add(position)
                    copiedPath = path.copy()
                    copiedPath.append(position)
                    queue.push(copiedPath)
        return None

class IDAstar:
    def __init__(self, dsFactory):
        self.dsFactory = dsFactory

    def findPath(self, pointA, pointB, mmap):
        stack = self.dsFactory("stack")
        bound = ManhattanDistance2D(pointA, pointB)
        stack.push(pointA)
        while True:
            t = self.IDA_star_search(pointB, stack, 0, bound, mmap)
            if t == "Found":
                return stack.getList()
            if t == None:
                return None
            bound = t

    def IDA_star_search(self, end, path, g, bound, mmap):
        node = path.peek()
        f = g + ManhattanDistance2D(node, end)
        if f > bound:
            return f
        if end == node:
            return "Found"
        minimum = None
        for neighbour in possiblePositions(node, mmap):
            if neighbour not in path.getList():
                path.push(neighbour)
                t = self.IDA_star_search(end, path, g + 1, bound, mmap)
                if t == "Found":
                    return "Found"
                if t != None:
                    if minimum == None:
                        minimum = t
                    elif t < minimum:
                        minimum = t                   
                path.pop()
        return minimum


