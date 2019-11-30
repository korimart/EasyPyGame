# REFERENCES (use the following)
#
# PathFinder class methods
#
#   findPath(pointA, pointB, mmap) -> returns a list of tuples from pointA to pointB
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

    def go(self, robot, mmap, pathFinder):
        # implement this
        # DO NOT check time and memory
        pass

class BehaviorAdpative:
    def __init__(self):
        self.dsFactory = AdaptiveDSFactory(self.memoryOverflow)
        self.algorithms = [BFS(self.dsFactory)] # add more according to your needs
        self.visitOrderProducer = VisitOrderProducer(self.algorithms[0])

    def go(self, robot, mmap, pathFinder):
        # implement this
        # check time and memory
        pass

    def memoryOverflow(self):
        # do not implement
        pass