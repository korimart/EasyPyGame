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
        while(len(mmap.getUnvisitedSearchPoints()) > 0):
            self._takeAStep(robot, mmap, pathFinder)

    def _takeAStep(self, robot, mmap, pathFinder):
        self.position = robot.getPos()
        self.direction = _posToDirection(self.position)
        self.coordinates = _posToCoord(self.position)
        mmap.pathTaken.append(self.coordinates)

        if len(mmap.pathTaken) == 0 and mmap.pathTaken[-1] != self.coordinates:
            self.pathNeedsUpdate = True

        if self.pathNeedsUpdate:
            mmap.pathToBeTaken = pathFinder.findPath(
                    self.coordinates, mmap.getUnvisitedSearchPoints(), mmap)
            if mmap.pathToBeTaken == None:
                raise RuntimeError("mmap.pathToBeTaken == None")
            self.pathNeedsUpdate = False

        if len(mmap.pathToBeTaken) == 0:
            mmap.update(
                self.coordinates,
                [],
                _getBlobData(robot, self.position))
            return

        self._faceThisPoint(robot, mmap.peekNextDestination())
        mmap.update(
                self.coordinates,
                self._getHazardData(robot, mmap),
                _getBlobData(robot, self.position))

        while(mmap.isOnNextStep()):
            mmap.pathToBeTaken = pathFinder.findPath(
                    self.coordinates, mmap.getUnvisitedSearchPoints(), mmap)
            if mmap.pathToBeTaken == None:
                raise RuntimeError("mmap.pathToBeTaken == None")
            self._faceThisPoint(robot, mmap.peekNextDestination())
            self._updateHazard(mmap, robot)

        mmap.popNextDestination()
        robot.move()

    def _faceThisPoint(self, robot, destination):
        while(destination != _calculateCoordinates(
            self.coordinates, self.direction)):
            robot.rotate()
            self.direction = _nextDirection(self.direction)

    def _updateHazard(self, mmap, robot):
        mmap.update(self.coordinates, self._getHazardData(robot, mmap), [])

    def _getHazardData(self, robot, mmap):
        hazards = []
        if robot.senseHazard():
                frontCoord = _calculateCoordinates(
                    self.coordinates, self.direction)
                hazards.append(frontCoord)
        return hazards

class BehaviorGoSlow:
    def __init__(self):
        self.pathNeedsUpdate = True
        self.position = None
        self.direction = None
        self.coordinates = None

    def go(self, robot, mmap, pathFinder):
        # implement this
        # DO NOT check time and memory
        self.visitOrderProducer = pathFinder
        while(len(mmap.getUnvisitedSearchPoints()) > 0):
            self._takeAStep(robot, mmap, pathFinder)

    def _takeAStep(self, robot, mmap, pathFinder):
        self._prepToMove(robot, mmap) #Base
        self._updateMap(robot, mmap) #Sub
        self._findPath(robot, mmap, pathFinder) #Sub
        self._move(robot, mmap) #Base

    def _prepToMove(self, robot, mmap):
        self.position = robot.getPos()
        self.direction = _posToDirection(self.position)
        self.coordinates = _posToCoord(self.position)
        mmap.pathTaken.append(self.coordinates)
        if len(mmap.pathTaken) == 0 and mmap.pathTaken[-1] != self.coordinates:
            self.pathNeedsUpdate = True

    def _findPath(self, robot, mmap, pathFinder):
        if mmap.isOnPath() or self.pathNeedsUpdate:
                mmap.pathToBeTaken = pathFinder.findPath(
                    self.coordinates, mmap.getUnvisitedSearchPoints(), mmap)
        self.pathNeedsUpdate = False
        if mmap.pathToBeTaken == None:
            raise RuntimeError("mmap.pathToBeTaken == None")

    def _move(self, robot, mmap):
        if len(mmap.pathToBeTaken) > 0:
                self._moveInDirection(robot, self.coordinates, self.direction,
                    mmap.popNextDestination())

    def _updateMap(self, robot, mmap):
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

    def _moveInDirection(self, robot, curLocation, direction, destination):
        #nextLocation = self.path.pop(0)
        while(destination != _calculateCoordinates(curLocation, direction)):
            robot.rotate()
            direction = _nextDirection(direction)
        robot.move()
