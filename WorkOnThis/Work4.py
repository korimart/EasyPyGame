# REFERENCES (use the following)
#
# PathFinder class methods
#
#   findPath(pointA, pointB, mmmap) -> returns a list of tuples from pointA to pointB
#
# Robot class methods
#
#   move() -> void
#   rotate() -> void
#   getPos() -> returns a tuple (x, y, direction)
#       direction is one of 0 (UP), 1 (RIGHT), 2 (DOWN), 3 (LEFT)
#   senseHazard() -> retruns a boolean
#   senseBlob() -> returns a list of 4 tuples (UP, RIGHT, DOWN, LEFT)
# 
# VisitOrderProducer class methods
#
#   setAlgorithm(algorithm) -> void

class BehaviorGoFast:
    def __init__(self):
        self.dsFactory = DSFactory()
        self.algorithm = BFS(self.dsFactory)
        self.visitOrderProducer = VisitOrderProducer(self.algorithm)
        # 
        self.pathNeedsUpdate = True
        self.position = None
        self.direction = None
        self.coordinates = None

    def go(self, robot, mmap, pathFinder):
        # implement this
        # DO NOT check time and memory
        while(len(mmap.getUnvisitedSearchPoints()) > 0):
            self._takeAStep(robot, mmap)
    
    def _takeAStep(self, robot, mmap):
        self._prepToMove(robot, mmap) #Base
        self._updatemMap(robot, mmap) #Sub
        self._findPath(robot, mmap) #Sub
        self._move(robot, mmap) #Base

    def _posToCoord(self, position):
        return (position[0], position[1])

    def _prepToMove(self, robot, mmap):
        self.position = robot.getPos()
        self.direction = self._posToDirection(self.position)
        self.coordinates = self._posToCoord(self.position)
        mmap.pathTaken.append(self.coordinates)
        if self._posToCoord(mmap.currentPos()) != self.coordinates:
            self.pathNeedsUpdate = True
    
    def _move(self, robot, mmap):
        if len(mmap.pathToBeTaken) > 0:
                self._moveInDirection(robot, self.coordinates, self.direction, mmap.nextDestination())

    def _updatemMap(self, robot, mmap):
        mmap.update(
                self.coordinates,
                self._getHazardData(robot, mmap, self.position),
                self._getBlobData(robot, self.position))

    # Yet to be changed in SIM or Robot
    def _getBlobData(self, robot, position):
        blobs = []
        direction = 0
        coordinates = [position[0], position[1]]
        rawData = robot.senseBlob()
        
        for raw in rawData:
            if raw:
                blobs.append(self._calculateCoordinates(coordinates, direction))
            direction = (direction + 1) % 4
        return blobs

    def _findPath(self, robot, mmap):
        if mmap.isOnPath or self.pathNeedsUpdate:
                mmap.pathToBeTaken = self.visitOrderProducer.findPath(
                    self.coordinates, mmap.getUnvisitedSearchPoints(), mmap)
        if mmap.pathToBeTaken == None:
            raise RuntimeError("mmap.pathToBeTaken == None")
    
    def _getHazardData(self, robot, mmap, position):
        hazards = []
        direction = position[2]
        coordinates = [position[0], position[1]]
        
        if robot.senseHazard():
                frontCoord = self._calculateCoordinates(coordinates, direction)
                hazards.append(frontCoord)
        return hazards

    def _posToDirection(self, position):
        return position[2]
    
    def _calculateCoordinates(self, coord, direction):
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

    def _moveInDirection(self, robot, curLocation, direction, destination):
        #nextLocation = self.path.pop(0)
        while(destination != self._calculateCoordinates(curLocation, direction)):
            robot.rotate()
            direction = self._nextDirection(direction)
        robot.move()

    def _nextDirection(self, direction):
        return (direction + 1) % 4

class BehaviorAdpative:
    def __init__(self):
        self.dsFactory = AdaptiveDSFactory()
        self.algorithms = [BFS(self.dsFactory)] # add more according to your needs
        self.visitOrderProducer = VisitOrderProducer(self.algorithms[0])
        
    def go(self, robot, mmap, pathFinder):
        # implement this
        # check time and memory
        pass
