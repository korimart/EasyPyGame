# REFERENCES (use the following)
#
# Algorithm class methods
#   findPath(pointA, pointB, mmap) -> returns a list of tuples from pointA to pointB
#
# Map class methods:
#
#   map.getTerrain(x, y) -> returns 0 (nothing) or 1 (hazard)
#       out-of-scope values also return 1

class VisitOrderProducer:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def findPath(self, startingPoint, targetList, mmap):
        # implemenet this
        # startingPoint is a tuple
        # targetList is a list of tuples that need to be visited
        # mmap is a Map class instance
        # return an optimized path that starts from startingPoint and visits all tuples in targetList
        pass