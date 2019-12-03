from AddOn.Algorithm import *
from AddOn.DSFactory import *
import multiprocessing
import time

class AlgorithmPicker:

    _BFS = 0
    _IDAstar = 1

    def __init__(self, dsFactory, maxBytes, maxTime, minTries=1):
        self.maxTime = maxTime
        self.dsFactory = MemCheckDSFactory(TimeCheckDSFactory(dsFactory, maxTime, TimeoutError), maxBytes, self.memCallback)
        self.algorithms = [BFS(self.dsFactory), IDAstar(self.dsFactory)]
        self.currAlgoIndex = AlgorithmPicker._IDAstar
        self.fromBFS = False
        self.minTries = minTries
        self.numTries = 0

    def findPath(self, pointA, pointB, mmap):
        try:
            path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
            return path
            """
            if self.currAlgoIndex == AlgorithmPicker._BFS_MEM:
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                return path

            elif self.currAlgoIndex == AlgorithmPicker._IDAstar_TIME:
                if not self.fromBFS or self.numTries > self.minTries:
                    self.currAlgoIndex = AlgorithmPicker._BFS_MEM
                    path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                    print(path)
                    return path
            """
        except MemoryError:
            if self.currAlgoIndex == AlgorithmPicker._BFS:
                self.currAlgoIndex = AlgorithmPicker._IDAstar
                #self.fromBFS = True
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                return path
            elif isinstance(self.algorithms[self.currAlgoIndex], IDAstar):
                raise MemoryError

        except TimeoutError:
            if self.currAlgoIndex == AlgorithmPicker._IDAstar:
                #if not self.fromBFS or self.numTries > self.minTries:
                self.currAlgoIndex = AlgorithmPicker._BFS
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                #print(path)
                return path
            
    def memCallback(self):
        raise MemoryError


