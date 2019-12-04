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

class VisitOrderProducer:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def findPath(self, startingPoint, targetList, mmap):
        # implemenet this
        # startingPoint is a tuple
        # targetList is a list of tuples that need to be visited
        # mmap is a Map class instance
        # return an optimized path that starts from startingPoint and visits all tuples in targetList
        path = []
        while(len(targetList) != 0):
            paths = []
            for searchPoint in targetList:
                paths.append(self.algorithm.findPath(startingPoint, searchPoint, mmap))
                if paths[-1] == None:
                    return None
            subPath = min(paths, key=len)
            del subPath[0]
            if len(subPath) > 0:
                startingPoint = subPath[-1]
            targetList.remove(startingPoint)
            path += subPath
        return path

class BFS:
    def __init__(self, dsFactory):
        self.dsFactory = dsFactory

    def findPath(self, pointA, pointB, mmap):
        # implement this
        # pointA and pointB are tuples of length 2
        # return a list of points on the calculated path
        queue = self.dsFactory.getQueue()

        visited = self.dsFactory.getSet()
        queue.push([pointA])
        visited.add(pointA)
        while(len(queue) != 0):
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
        stack = self.dsFactory.getStack()
        bound = ManhattanDistance2D(pointA, pointB)
        stack.push(pointA)
        while True:
            t = self._IDA_star_search(pointB, stack, 0, bound, mmap)
            if t == "Found":
                return stack.getList()
            if t == None:
                return None
            bound = t

    def _IDA_star_search(self, end, path, g, bound, mmap):
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
                t = self._IDA_star_search(end, path, g + 1, bound, mmap)
                if t == "Found":
                    return "Found"
                if t != None:
                    if minimum == None:
                        minimum = t
                    elif t < minimum:
                        minimum = t
                path.pop()
        return minimum