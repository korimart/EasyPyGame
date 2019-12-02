from AddOn.Algorithm import *
from AddOn.DSFactory import *
import time

class AlgorithmPicker:

    _BFS_INDEX = 0
    _IDAstar_INDEX = 1
    
    def __init__(self, dsFactory, maxBytes, maxTime):
        self.maxTime = maxTime
        self.dsFactory = MemCheckDSFactory(dsFactory, maxBytes, self.memCallback)
        self.algorithms = [BFS(self.dsFactory), IDAstar(self.dsFactory)]
        self.currAlgoIndex = 0

        # and other members as necessary

    def findPath(self, pointA, pointB, mmap):

        try:
            t_start = time.time()
            path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
            t_delta = time.time() - t_start()

        except MemoryError:
            # implement this
            # change algorithm and try again
            if isinstance(self.algorithms[self.currAlgoIndex], BFS):
                self.currAlgoIndex = AlgorithmPicker._IDAstar_INDEX
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
            

        # also use Python's whatever event system for max time
        # change alogirhtm and try again
        if t_delta > self.maxTime:
            if isinstance(self.algorithms[self.currAlgoIndex], BFS):
                self.currAlgoIndex = AlgorithmPicker._IDAstar_INDEX
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
        
        return path

    def memCallback(self):
        raise MemoryError
