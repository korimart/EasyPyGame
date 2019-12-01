from AddOn.Algorithm import *
from AddOn.DSFactory import *

def _IDAstar_INDEX():
    return 1

def _BFS_INDEX():
    return 0

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
            if isinstance(self.algorithms[self.currAlgoIndex], BFS):
                self.currAlgoIndex = _IDAstar_INDEX()
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)

        # also use Python's whatever event system for max time
        # change alogirhtm and try again
        except TimeoutError:
            if isinstance(self.algorithms[self.currAlgoIndex], BFS):
                self.currAlgoIndex = _IDAstar_INDEX()
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
        
        return path

    def memCallback(self):
        raise MemoryError

#TEST
"""
if __name__ == "__main__":
    picker = AlgorithmPicker(DSFactory(), 200, 100)
    picker.findPath(...)
"""