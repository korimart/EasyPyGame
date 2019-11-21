from abc import ABC, abstractmethod
import sys
from pympler import asizeof

class AddOn:
    def __init__(self, size, hazards, searchPoints, robot):
        self.map = Map(size, hazards, searchPoints, robot)
        self.pathFinder = bfsShortestFirst()
        self.behavior = GoSlow(self.map)
        self.robot = robot
        
    def go(self, robot):
        self.behavior.go(robot, self.map, self.pathFinder)


class Behavior(ABC):
    def __init__(self, map):
        self.path = []
        self.pathNeedsUpdate = True
        self.searchPoints = map.getUnvisitedSearchPoints()

    @abstractmethod
    def go(self, robot, map, pathFinder):
        pass

    def getHazardDataInAllDirections(self, robot, map, position):
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



class GoSlow(Behavior):
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
            if len(map.pathToBeTaken) > 0:
                self.moveInDirection(robot, coordinates, direction, map.nextDestination())
            

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

class PathFinder:
    def __init__(self, path=[], paths=[], queue=[], print = lambda : None):
        self.path = path
        self.paths = paths
        self.queue = queue
        self.print = print

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
        
    def bfs(self, minInclusive, maxExclusive, forbidden, start, end):
        del self.queue[:]
        visited = set()
        self.queue.append([start])
        visited.add(start)
        while(len(self.queue) != 0):
            self.print()
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
        return [None]
    
    def adaptiveBfs(self, minInclusive, maxExclusive, forbidden, start, end, limit):
        del self.queue[:]
        visited = set()
        self.queue.append([start])
        visited.add(start)
        sizeReached = 0
        curSize = asizeof.asizeof(self.queue)
        while(curSize < limit and len(self.queue) != 0):
            if curSize > sizeReached:
                sizeReached = curSize
            self.print()
            path = self.queue.pop(0)
            current = path[-1]
            if end == current:
                del self.queue[:]
                return [path, sizeReached]
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
            return [None, sizeReached]
    
    def adaptiveShortestFirst(self, minInclusive, maxExclusive, forbidden,
    start, searchPoints, searchAlgorithm, limit):
        maxSize = 0
        while(len(searchPoints) != 0):
            del self.paths[:]
            del self.queue[:]
            for searchPoint in searchPoints:
                result = searchAlgorithm(minInclusive, maxExclusive,
                forbidden, start, searchPoint, limit)
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
        return [pathToBeReturned, maxSize]

    def shortestFirst(self, minInclusive, maxExclusive, forbidden,
    start, searchPoints, searchAlgorithm):
        while(len(searchPoints) != 0):
            del self.paths[:]
            del self.queue[:]
            for searchPoint in searchPoints:
                self.paths.append(searchAlgorithm(minInclusive, maxExclusive,
                forbidden, start, searchPoint))
            subPath = min(self.paths, key=len)
            del subPath[0]
            if len(subPath) > 0:
                start = subPath[-1]
            searchPoints.remove(start)
            self.path += subPath
        pathToBeReturned = self.path.copy()
        self.empty()
        return pathToBeReturned

class SimableAddOn(AddOn):
    def __init__(self,  map, size, hazards, searchPoints, sim,
        path, paths, queue):
        super().__init__(self,  map, size, hazards, searchPoints, sim)
        self.pathFinder = SIM_bfsShortestFirst(path, paths, queue, sim.printPaths)


class bfsShortestFirst(PathFinder):        
    def findPath(self, map, start):
        return self.shortestFirst(map.minPoints, map.size,
                    map.hazards, start, map.getUnvisitedSearchPoints(), self.bfs)

#there's really not much of a difference btw SIM_bfsShortest and bfsShortest
class SIM_bfsShortestFirst(PathFinder):
    def __init__(self, path, paths, queue, print):
        super().__init__(path, paths, queue, print)

    def findPath(self, map, start):
        return self.shortestFirst(map.minPoints, map.size,
                    map.hazards, start, map.getUnvisitedSearchPoints(), self.bfs)


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
    def __init__(self, size, hazards, searchPoints, robot, minPoints=(0,0)):
        self.hazards = self.initHazards(hazards)
        self.searchPoints = set(searchPoints)
        self.visitedSearchPoints = set()
        self.unvisitedSearchPoints = set(searchPoints)
        self.blobs = []
        self.robot = robot
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
        
    def update(self, robot, hazards=[], blobs=[]):
        for h in hazards:
            self.hazards[h] = 1
        for b in blobs:
            if b in self.blobs:
                pass
            else:
                self.blobs.append()
        self.robot = robot
        if robot in self.searchPoints:
            self.visitedSearchPoints.add(robot)
            self.unvisitedSearchPoints.remove(robot)
    
    def isOnPath(self):
        for p in self.pathToBeTaken:
            if p in self.hazards:
                return True
            else:
                return False

    def nextDestination(self):
        return self.pathToBeTaken.pop(0)

    def currentPos(self):
        return self.robot
    
    def getVisitedSearchPoints(self):
        return self.visitedSearchPoints
    
    def setVisitedSearchPoints(self, location):
        self.visitedSearchPoints.add(location)
    
    def getUnvisitedSearchPoints(self):
        return self.unvisitedSearchPoints.copy()

