from AddOn.DSFactory import *
from AddOn.Algorithm import *

def _posToCoord(position):
        return (position[0], position[1])

def _posToDirection(position):
        return position[2]

def _calculateCoordinates(coord, direction):
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

def _nextDirection(direction):
        return (direction + 1) % 4

def _getBlobData(robot, position):
        blobs = []
        direction = 0
        coordinates = [position[0], position[1]]
        rawData = robot.senseBlob()

        for raw in rawData:
            if raw:
                blobs.append(_calculateCoordinates(coordinates, direction))
            direction = (direction + 1) % 4
        return blobs


class BehaviorGoFast:
    def __init__(self):
        self.pathNeedsUpdate = True
        self.position = None
        self.direction = None
        self.coordinates = None

    def go(self, robot, mmap, pathFinder):
        # implement this
        # DO NOT check time and memory
        while(len(mmap.getUnvisitedSearchPoints()) > 0):
            self._takeAStep(robot, mmap, pathFinder)

    def _takeAStep(self, robot, mmap, pathFinder):
        self._prepToMove(robot, mmap) #Base
        self._updatemMap(robot, mmap) #Sub
        self._findPath(robot, mmap, pathFinder) #Sub
        self._move(robot, mmap) #Base

    def _prepToMove(self, robot, mmap):
        self.position = robot.getPos()
        self.direction = _posToDirection(self.position)
        self.coordinates = _posToCoord(self.position)
        mmap.pathTaken.append(self.coordinates)
        if _posToCoord(mmap.currentPos()) != self.coordinates:
            self.pathNeedsUpdate = True

    def _findPath(self, robot, mmap, pathFinder):
        if mmap.isOnPath or self.pathNeedsUpdate:
                mmap.pathToBeTaken = pathFinder.findPath(
                    self.coordinates, mmap.getUnvisitedSearchPoints(), mmap)
        if mmap.pathToBeTaken == None:
            raise RuntimeError("mmap.pathToBeTaken == None")

    def _move(self, robot, mmap):
        if len(mmap.pathToBeTaken) > 0:
                self._moveInDirection(robot, self.coordinates, self.direction, mmap.nextDestination())

    def _updatemMap(self, robot, mmap):
        mmap.update(
                self.coordinates,
                self._getHazardData(robot, mmap, self.position),
                _getBlobData(robot, self.position))

    def _getHazardData(self, robot, mmap, position):
        hazards = []
        direction = position[2]
        coordinates = [position[0], position[1]]
        
        if robot.senseHazard():
                frontCoord = _calculateCoordinates(coordinates, direction)
                hazards.append(frontCoord)
        for i in range(3):
            robot.rotate()
            direction = (direction + 1) % 4
            if robot.senseHazard():
                frontCoord = _calculateCoordinates(coordinates, direction)
                hazards.append(tuple(frontCoord))
        self.direction = (self.direction + 3) % 4
        return hazards
        """
        hazards = []
        direction = position[2]
        coordinates = [position[0], position[1]]

        if robot.senseHazard():
                frontCoord = self._calculateCoordinates(coordinates, direction)
                hazards.append(frontCoord)
        return hazards
        """

    def _moveInDirection(self, robot, curLocation, direction, destination):
        #nextLocation = self.path.pop(0)
        while(destination != _calculateCoordinates(curLocation, direction)):
            robot.rotate()
            direction = _nextDirection(direction)
        robot.move()

