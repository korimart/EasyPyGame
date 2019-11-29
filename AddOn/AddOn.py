from abc import ABC, abstractmethod
import sys
import time
from pympler import asizeof

class PathAlgorithm:
    def __init__(self, path=[], paths=[], queue=[]):
        self.path = path
        self.paths = paths
        self.queue = queue

    def empty(self):
        del self.path[:]
        del self.paths[:]
        del self.queue[:]

    def sanitiyCheck(self, minInclusive, maxExclusive, forbidden, locations):
        lst = []
        for p in locations:
            if p not in forbidden and minInclusive[0] <= p[0] < maxExclusive[0] and minInclusive[1] <= p[1] < maxExclusive[1]:
                lst.append(p)
        return lst
        """
        return [p if p in forbidden and
            minInclusive[0] <= p[0] < maxExclusive[0] and
            minInclusive[1] <= p[1] < maxExclusive[1]
            else None for p in locations]
        """
    
    def calculateCoordinates(self, coord, direction):
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

    def possiblePositions(self, minInclusive, maxExclusive, forbidden, curPos):
        positions = list()
        for dir in range(4):
            positions.append(self.calculateCoordinates(curPos, dir))
        return self.sanitiyCheck(minInclusive, maxExclusive,
            forbidden, positions)
        
    def bfs(self, minInclusive, maxExclusive, forbidden, start, end, print = lambda : None):
        del self.queue[:]
        visited = set()
        self.queue.append([start])
        visited.add(start)
        while(len(self.queue) != 0):
            print()
            path = self.queue.pop(0)
            current = path[-1]
            if end == current:
                del self.queue[:]
                return path
            possiblePositions = self.possiblePositions(minInclusive,
            maxExclusive, forbidden, current)
            for position in possiblePositions:
                if position not in visited:
                    visited.add(position)
                    copiedPath = path.copy()
                    copiedPath.append(position)
                    self.queue.append(copiedPath)
        del self.queue[:]
        return None
    
    def adaptiveBfs(self, minInclusive, maxExclusive, forbidden, start, end, limit, print = lambda : None):
        timeStart = time.time()
        del self.queue[:]
        visited = set()
        self.queue.append([start])
        visited.add(start)
        sizeReached = 0
        curSize = asizeof.asizeof(self.queue)
        while(curSize < limit and len(self.queue) != 0):
            if curSize > sizeReached:
                sizeReached = curSize
            print()
            path = self.queue.pop(0)
            current = path[-1]
            if end == current:
                del self.queue[:]
                return [path, sizeReached, time.time()-timeStart]
            possiblePositions = self.possiblePositions(minInclusive,
            maxExclusive, forbidden, current)
            for position in possiblePositions:
                if position not in visited:
                    visited.add(position)
                    copiedPath = path.copy()
                    copiedPath.append(position)
                    self.queue.append(copiedPath)
            curSize = asizeof.asizeof(self.queue)
        if curSize > limit:
            del self.queue[:]
            raise MemoryError("curSize " + str(curSize) + " > " + "limit " + str(limit))
        else:
            del self.queue[:]
            return [None, sizeReached, time.time()-timeStart]
    
    def adaptiveShortestFirst(self, minInclusive, maxExclusive, forbidden,
    start, searchPoints, searchAlgorithm, limit, print = lambda : None):
        timeStart = time.time()
        maxSize = 0
        while(len(searchPoints) != 0):
            del self.paths[:]
            del self.queue[:]
            for searchPoint in searchPoints:
                result = searchAlgorithm(minInclusive, maxExclusive,
                forbidden, start, searchPoint, limit, print=print)
                if result[0] == None:
                    self.empty()
                    return None
                self.paths.append(result[0])
                if result[1] > maxSize:
                    maxSize = result[1]
            subPath = min(self.paths, key=len)
            del subPath[0]
            start = subPath[-1]
            searchPoints.remove(start)
            self.path += subPath
        pathToBeReturned = self.path.copy()
        self.empty()
        return [pathToBeReturned, maxSize, time.time()-timeStart]

    def shortestFirst(self, minInclusive, maxExclusive, forbidden,
    start, searchPoints, searchAlgorithm, print = lambda : None):
        while(len(searchPoints) != 0):
            del self.paths[:]
            del self.queue[:]
            for searchPoint in searchPoints:
                self.paths.append(searchAlgorithm(minInclusive, maxExclusive,
                forbidden, start, searchPoint, print=print))
                if self.paths[-1] == None:
                    self.empty()
                    return None
            subPath = min(self.paths, key=len)
            del subPath[0]
            if len(subPath) > 0:
                start = subPath[-1] 
            searchPoints.remove(start)
            self.path += subPath
        pathToBeReturned = self.path.copy()
        self.empty()
        return pathToBeReturned

    def ManhattanDistance2D(self, x1, x2):
        d = 0
        d += abs(x1[0] - x2[0])
        d += abs(x1[1] - x2[1])
        return d

    def adaptiveIDA_star(self, minInclusive, maxExclusive, forbidden,
        start, end, limit=1, print = lambda : None):
        startTime = time.time()
        path = self.IDA_star(minInclusive, maxExclusive, forbidden, start, end)
        return [path, 0, time.time() - startTime]

    # it needs to follow shortestFirst's searchAlgorithm's arguments
    # def IDA_star(self, start, goal, h, cost, succeessors):
    def IDA_star(self, minInclusive, maxExclusive, forbidden,
        start, end, print = lambda : None):
        bound = self.ManhattanDistance2D(start, end)
        del self.queue[:]
        self.queue.append(start)
        while True:
            t = self.IDA_star_search(end, self.queue, 0, bound,
                minInclusive, maxExclusive, forbidden)
            if t == "Found":
                return self.queue.copy()
            if t == -1:
                return None
            bound = t

    def IDA_star_search(self, end, path, g, bound,
        minInclusive, maxExclusive, forbidden):
        node = path[-1]
        f = g + self.ManhattanDistance2D(node, end)
        if f > bound:
            return f
        if end == node:
            return "Found"
        min = None
        for next in self.possiblePositions(minInclusive, maxExclusive, forbidden, node):
            if next not in path:
                path.append(next)
                t = self.IDA_star_search(end, path, g + 1, bound,
                    minInclusive, maxExclusive, forbidden)
                if t == "Found":
                    return "Found"
                if t != None:
                    if min == None:
                        min = t
                    elif t < min:
                        min = t                   
                path.pop(-1)
        return min


class AddOn:
    def __init__(self, size, hazards, searchPoints, robotLocation, behavior):
        self.map = Map(size, hazards, searchPoints, robotLocation)
        #self.pathFinder = pathFinder
        self.behavior = behavior
        self.robotLocation = robotLocation
        
    def go(self, robot):
        self.behavior.go(robot, self.map)


class Behavior(ABC):
    def __init__(self, pathFinder):
        self.path = []
        self.pathNeedsUpdate = True
        #self.searchPoints = map.getUnvisitedSearchPoints()
        self.position = None
        self.direction = None
        self.coordinates = None
        self.pathFinder = pathFinder

    def go(self, robot, map):
        while(len(map.getUnvisitedSearchPoints()) > 0):
            self.takeAStep(robot, map)
    
    def takeAStep(self, robot, map):
        self.prepToMove(robot, map) #Base
        self.updateMap(robot, map) #Sub
        self.findPath(robot, map) #Sub
        self.move(robot, map) #Base

    def prepToMove(self, robot, map):
        self.position = robot.getPos()
        self.direction = self.posToDirection(self.position)
        self.coordinates = self.posToCoord(self.position)
        map.pathTaken.append(self.coordinates)
        if self.posToCoord(map.currentPos()) != self.coordinates:
            self.pathNeedsUpdate = True
    
    def move(self, robot, map):
        if len(map.pathToBeTaken) > 0:
                self.moveInDirection(robot, self.coordinates, self.direction, map.nextDestination())

    @abstractmethod
    def updateMap(self,robot, map):
        pass

    @abstractmethod
    def findPath(self, robot, map):
        pass

    @abstractmethod
    def getHazardData(self, robot, map, position):
        pass
    
    def calculateCoordinates(self, coord, direction):
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

    def sanityCheck(self, minInclusive, maxExclusive, location):
            if (minInclusive[0] <= location[0] < maxExclusive[0]) and (minInclusive[1] <= location[1] < maxExclusive[1]):
                return True
            else:
                return False
            
    """
    def sanityCheck(self, map, coord):
        if coord[0] >= map.size[0] or coord[0] < 0:
            return False
        elif coord[1] >= map.size[1] or coord[1] < 0:
            return False
        else:
            return True
    """

    def nextDirection(self, direction):
        return (direction + 1) % 4

    def getBlobData(self, robot, position):
        blobs = []
        direction = position[2]
        coordinates = [position[0], position[1]]
        rawData = robot.senseBlob()
        
        for raw in rawData:
            if raw:
                blobs.append(self.calculateCoordinates(coordinates, direction))
                #self.sanityCheck(map.minPoints, map.size, coordinates)
                
            direction = (direction + 1) % 4
        return blobs

    def getCoordinates(self, robot):
        pos = robot.getPos()
        return (pos[0], pos[1])

    def getDirection(self, robot):
        pos = robot.getPos()
        return pos[2]

    def posToCoord(self, position):
        return (position[0], position[1])
    
    def posToDirection(self, position):
        return position[2]

    def moveInDirection(self, robot, curLocation, direction, destination):
        #nextLocation = self.path.pop(0)
        while(destination != self.calculateCoordinates(curLocation, direction)):
            robot.rotate()
            direction = self.nextDirection(direction)
        robot.move()
"""
go:
    while :
        takeAStep

takeAStep:
    doPrepToMove: BASE
    updateMap: SUB
    findPath: SUB
    move: BASE
"""
class GoSlow(Behavior):
    """
    def go(self, robot, map, pathFinder):
        while(len(map.getUnvisitedSearchPoints()) > 0):

            position = robot.getPos()
            direction = self.posToDirection(position)
            coordinates = self.posToCoord(position)
            map.pathTaken.append(coordinates)
            if self.posToCoord(map.currentPos()) != coordinates:
                self.pathNeedsUpdate = True

            map.update(
                coordinates,
                self.getHazardDataInAllDirections(robot, map, position),
                self.getBlobData(robot, position))
            direction = (direction + 3) % 4

            #checks if the path needs an update
            if map.isOnPath or self.pathNeedsUpdate:
                map.pathToBeTaken = pathFinder.findPath(map, coordinates)
            if map.pathToBeTaken == None:
                raise RuntimeError("map.pathToBeTaken == None")
            if len(map.pathToBeTaken) > 0:
                self.moveInDirection(robot, coordinates, direction, map.nextDestination())
    """
    
    def updateMap(self, robot, map):
        map.update(
                self.coordinates,
                self.getHazardData(robot, map, self.position),
                self.getBlobData(robot, self.position))
        self.direction = (self.direction + 3) % 4

    def findPath(self, robot, map):
        if map.isOnPath or self.pathNeedsUpdate:
                map.pathToBeTaken = self.pathFinder.findPath(map, self.coordinates)
        if map.pathToBeTaken == None:
            raise RuntimeError("map.pathToBeTaken == None")
    
    def getHazardData(self, robot, map, position):
        hazards = []
        direction = position[2]
        coordinates = [position[0], position[1]]
        
        if robot.senseHazard():
                frontCoord = self.calculateCoordinates(coordinates, direction)
                #I'm not sure why it needs to be checked
                if self.sanityCheck(map.minPoints, map.size, frontCoord):
                    hazards.append(frontCoord)
        for i in range(3):
            robot.rotate()
            direction = (direction + 1) % 4
            if robot.senseHazard():
                frontCoord = self.calculateCoordinates(coordinates, direction)
                #I'm not sure why it needs to be checked
                if self.sanityCheck(map.minPoints, map.size, frontCoord):
                    hazards.append(tuple(frontCoord))
        return hazards

class PathFinder:
    def __init__(self):
        self.pathFinder = PathAlgorithm()
    @abstractmethod
    def findPath(self):
        pass

class AdaptivePathFinder(PathFinder):
    def __init__(self, memoryLimit):
        super().__init__()
        self.lastMemoryUsage = 0
        self.lastTimeUsage = 0
        self.memoryLimit = memoryLimit
    
    def getLastMemoryUsage(self):
        return self.lastMemoryUsage
    
    def getLastTimeUsage(self):
        return self.lastTimeUsage


class AdaptiveBfsShortestFirst(AdaptivePathFinder):
    def findPath(self, map, start):
        result = self.pathFinder.adaptiveShortestFirst(map.minPoints, map.size,
                    map.hazards, start, map.getUnvisitedSearchPoints(),
                    self.pathFinder.adaptiveBfs, limit=self.memoryLimit)
        self.lastMemoryUsage = result[1]
        self.lastTimeUsage = result[2]
        return result[0]

class AdaptiveIDA_starShortestFirst(AdaptivePathFinder):
    def findPath(self, map, start):
        result = self.pathFinder.adaptiveShortestFirst(map.minPoints, map.size,
                    map.hazards, start, map.getUnvisitedSearchPoints(),
                    self.pathFinder.adaptiveIDA_star, limit=self.memoryLimit)
        self.lastMemoryUsage = result[1]
        self.lastTimeUsage = result[2]
        return result[0]

class AdaptiveGoSlow(GoSlow):
    def __init__(self, memoryThreshold, timeThreshold, pathFinder):
        super().__init__(pathFinder)
        self.memoryThreshold = memoryThreshold
        self.timeThreshold = timeThreshold

    def findPath(self, robot, map):
        super().findPath(robot, map)
        if self.pathFinder.getLastMemoryUsage() > self.memoryThreshold:
            print("BFS -> IDA star. Cause: memory ", self.pathFinder.getLastMemoryUsage())
            self.pathFinder = AdaptiveIDA_starShortestFirst(self.pathFinder.memoryLimit)
        if (self.pathFinder.getLastTimeUsage() > self.timeThreshold
            and isinstance(self.pathFinder, AdaptiveBfsShortestFirst)):
            print("BFS -> IDA star. Cause: time ", self.pathFinder.getLastTimeUsage())
            self.pathFinder = AdaptiveIDA_starShortestFirst(self.pathFinder.memoryLimit)
            
    


"""
psuedocode for bfs:
function bfs(map, start, end)
initialize: Set: visited, Queue: queue
push a list with the start position in it to the queue
while the queue is not empty:
    path = queue.dequeue()
    current = path[-1]
    visited.add(current)
    if end == current:
        return path
    calculate the list of possible positions the robot can take from current
    for each position in the list: 
        if a position is not in the visited set:
            copy the path and push the position to the copied path
            push the copied path to the queue
"""


class IDA_starShortestFirst():
    def __init__(self):
        self.pathFinder = PathAlgorithm()   
    def findPath(self, map, start):
        return self.pathFinder.shortestFirst(map.minPoints, map.size,
                    map.hazards, start, map.getUnvisitedSearchPoints(), self.pathFinder.IDA_star)


class SIM_PathAlgorithm(PathAlgorithm):
    def print(self):
        # print path
        pass


class SimableAddOn(AddOn):
    def __init__(self,  map, size, hazards, searchPoints, sim,
        path, paths, queue):
        super().__init__(self,  map, size, hazards, searchPoints, sim)
        self.pathFinder = SIM_bfsShortestFirst()


class bfsShortestFirst2():
    def __init__(self):
        self.path = []
        self.paths = []
        self.queue = []
        self.pathFinder = PathAlgorithm(path=self.path, paths=self.paths, queue=self.queue)

    def print(self):
        #print paths
        pass
    
    def findPath(self, map, start):
        return self.pathFinder.shortestFirst(map.minPoints, map.size,
                    map.hazards, start, map.getUnvisitedSearchPoints(), self.print)
    

class bfsShortestFirst:
    def __init__(self):
        self.pathFinder = PathAlgorithm()   
    def findPath(self, map, start):
        return self.pathFinder.shortestFirst(map.minPoints, map.size,
                    map.hazards, start, map.getUnvisitedSearchPoints(), self.pathFinder.bfs)

class SIM_bfsShortestFirst():
    def __init__(self):
        self.pathFinder = SIM_PathAlgorithm()   
    def findPath(self, map, start):
        return self.pathFinder.shortestFirst(map.minPoints, map.size,
                    map.hazards, start, map.getUnvisitedSearchPoints(), self.pathFinder.bfs,
                    self.pathFinder.print)


    """ kept just in case 
    def findPath(self, map, start):
        searchPoints = set(map.searchPoints)
        path = []
        while(len(searchPoints) != 0):
            paths = []
            for searchPoint in searchPoints:
                paths.append(self.bfs(map.minPoints, map.size,
                    map.hazards, start, searchPoint))
            subPath = min(paths, key=len)
            del subPath[0]
            usedSearchPoint = subPath[-1]
            searchPoints.remove(usedSearchPoint)
            path += subPath
        return path
    """


class Map:
    def __init__(self, size, hazards, searchPoints, robotLocation, minPoints=(0,0)):
        self.hazards = self.initHazards(hazards)
        self.searchPoints = set(searchPoints)
        self.visitedSearchPoints = set()
        self.unvisitedSearchPoints = set(searchPoints)
        self.blobs = set()
        self.robotLocation = robotLocation
        self.size = size
        self.pathTaken = []
        self.pathToBeTaken = []
        self.minPoints = minPoints

    def initHazards(self, points):
        d = {}
        for p in points:
            d[p] = 1
        return d

    #should be deleted
    def initList(self, size, points):
        x = size[0]
        y = size[1]
        l = [ [0] * y for i in range(x)]
        for p in points:
            l[p[0]][p[1]] = 1
        
    def update(self, robotLocation, hazards=[], blobs=[]):
        for h in hazards:
            self.hazards[h] = 1
        for b in blobs:
            if b in self.blobs:
                pass
            else:
                self.blobs.add(b)
        self.robotLocation = robotLocation
        if robotLocation in self.searchPoints:
            self.visitedSearchPoints.add(robotLocation)
            if robotLocation in self.unvisitedSearchPoints:
                self.unvisitedSearchPoints.remove(robotLocation)
    
    def isOnPath(self):
        for p in self.pathToBeTaken:
            if p in self.hazards:
                return True
            else:
                return False

    def nextDestination(self):
        return self.pathToBeTaken.pop(0)

    def currentPos(self):
        return self.robotLocation
    
    def getVisitedSearchPoints(self):
        return self.visitedSearchPoints
    
    def setVisitedSearchPoints(self, location):
        self.visitedSearchPoints.add(location)
    
    def getUnvisitedSearchPoints(self):
        return self.unvisitedSearchPoints.copy()

    def getTerrain(self, pos):
        if pos in self.hazards:
            return 1
        if pos[0] < self.minPoints[0]:
            return 1
        if pos[1] < self.minPoints[1]:
            return 1
        if pos[0] >= self.size[0]:
            return 1
        if pos[0] >= self.size[0]:
            return 1
        return 0
        

