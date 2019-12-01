from AddOn.Algorithm import *
from AddOn.DSFactory import *

class AlgorithmPicker:
    def __init__(self, dsFactory, maxBytes, maxTime):
        self.maxTime = maxTime
        self.dsFactory = MemCheckDSFactory(dsFactory, maxBytes, self.memCallback)
        self.algorithms = [BFS(self.dsFactory), IDAstar(self.dsFactory)]
        self.currAlgoIndex = 0

        # and other members as necessary

    def findPath(self, pointA, pointB, mmap):
        try:
            path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
        except MemoryError:
            # implement this
            # change algorithm and try again
            pass

        # also use Python's whatever event system for max time
        # change alogirhtm and try again

        return path

    def memCallback(self):
        raise MemoryError