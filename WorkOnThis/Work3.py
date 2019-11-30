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
        while(len(targetList) != 0):
            paths = []
            path = []
            for searchPoint in targetList:
                paths.append(self.algorithm(startingPoint, searchPoint, mmap))
                if paths[-1] == None:
                    return None
            subPath = min(paths, key=len)
            del subPath[0]
            if len(subPath) > 0:
                PointA = subPath[-1] 
            targetList.remove(PointA)
            path += subPath
        return path