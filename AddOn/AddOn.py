from abc import ABC, abstractmethod

class AddOn:
    def __init__(self,  map, size, hazards, searchPoints, robot):
        self.map = (size, hazards, searchPoints, robot)
        self.pathFinder = bfsShortestFirst()
        self.behavior = GoFast()
        self.robot = robot

    def go(self, robot):
        self.behavior.go(self.robot, self.map, self.pathFinder)


class Behavior(ABC):
    def __init__(self, map):
        self.path = []
        self.pathNeedsUpdate = True
        self.searchPoints = map.getSearchPoints

    @abstractmethod
    def go(self, robot, map, pathfinder):
        pass

    def getHazardData(self, robot, map, position):
        hazards = []
        direction = position[2]
        coordinates = [position[0], position[1]]
        
        if robot.senseHazard():
                frontCoord = self.calculateCoordinates(coordinates, direction)
                if self.sanityCheck(map, frontCoord):
                    hazards.append(frontCoord)
        for i in range(3):
            robot.rotate()
            direction = (direction + i) % 4
            if robot.senseHazard():
                frontCoord = self.calculateCoordinates(coordinates, direction)
                if self.sanityCheck(map, frontCoord):
                    hazards.append(frontCoord)
        return hazards
    
    def calculateCoordinates(self, coord, direction):
        newCoord = coord.copy()
        if direction == 0:
            newCoord[1] += 1 
        elif direction == 1:
           newCoord[0] += 1
        elif direction == 2:
            newCoord[1] -= 1
        elif direction == 3:
            newCoord[0] -= 1
        return newCoord

    def sanityCheck(self, map, coord):
        if coord[0] >= map.size[0] or coord[0] < 0:
            return False
        elif coord[1] >= map.size[1] or coord[1] < 0:
            return False
        else:
            return True

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
                self.sanityCheck(map, coordinates)
                
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

    def moveInDirection(self, robot, curLocation, direction):
        nextLocation = self.path.pop(0)
        while(nextLocation != self.calculateCoordinates(curLocation, direction)):
            robot.rotate()
        robot.move()



class GoFast(Behavior):
    def __init__(self):
        super.__init__()
    
    def go(self, robot, map, pathfinder):
        position = robot.getPos()
        direction = self.posToCoord(position)
        coordinates = self.posToDirection
        map.pathTaken.append(coordinates)
        if self.posToCoord(map.currentPos()) != coordinates:
            self.pathNeedsUpdate = True
        map.update(self.getHazardData(robot, map, coordinates),
            self.getBlobData(robot, position), robot.getPos())
        
        #checks if the path needs an update
        if map.isOnPath or self.pathNeedsUpdate:
            self.path = pathfinder.findPath(map)

        self.moveInDirection(robot, coordinates, direction)
            

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

class PathFinder(ABC):
    def __init__(self):
        pass
    
    def sanitiyCheck(self, map, locations):
        return [p if p in map.hazards and
            0 <= p[0] < map.size[0] and
            0 <= p[1] < map.size[1]
            else None for p in locations]
    
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

    def possiblePositions(self, map, curPos):
        positions = list()
        for dir in range(4):
            positions.append(self.calculateCoordinates(curPos, dir))
        return self.sanitiyCheck(map, positions)
        
    def bfs(self, map, start, end):
        visited = set()
        queue = [start]
        while(len(queue) != 0):
            path = queue.pop()
            current = path[-1]
            if end == current:
                return path
            possiblePositions = self.possiblePositions(map, current)
            for position in possiblePositions:
                if position not in visited:
                    copiedPath = path.copy()
                    copiedPath.append(position)
                    queue.append(copiedPath)
        return False

    @abstractmethod
    def findPath(self, map, start):
        pass

class bfsShortestFirst(PathFinder):
    def findPath(self, map, start):
        searchPoints = set(map.searchPoints)
        path = []
        while(len(searchPoints) != 0):
            paths = []
            for searchPoint in searchPoints:
                paths.append(self.bfs(map, start, searchPoint))
            subPath = min(paths, key=len)
            del subPath[0]
            usedSearchPoint = subPath[-1]
            searchPoints.remove(usedSearchPoint)
            path += subPath
        return path 


class Map:
    def __init__(self, size, hazards, searchPoints, robot):
        self.hazards = self.initHazards(hazards)
        self.searchPoints = set(searchPoints)
        self.visitedSearchPoints = set()
        self.blobs = []
        self.robot = robot
        self.size = size
        self.pathTaken = []
        self.pathToBeTaken = []

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
        
    def update(self, hazards, blobs, robot, searchPoint):
        for h in hazards:
            self.hazards[h] = 1
        for b in blobs:
            if b in self.blobs:
                pass
            else:
                self.blobs.append()
        self.robot = robot
        if searchPoint != None:
            self.visitedSearchPoints.add(searchPoint)
    
    def isOnPath(self, path):
        for p in path:
            if p in self.hazards:
                return True
            else:
                return False

    def currentPos(self):
        return self.robot
    
    def getVisitedSearchPoints(self):
        return self.visitedSearchPoints
    
    def setVisitedSearchPoints(self, location):
        self.visitedSearchPoints.add(location)
    
    
