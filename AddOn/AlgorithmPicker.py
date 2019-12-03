from AddOn.Algorithm import *
from AddOn.DSFactory import *
import multiprocessing
import time

class AlgorithmPicker:

    _BFS_MEM = 0
    _IDAstar_MEM = 1
    _BFS_TIME = 2
    _IDAstar_TIME = 3

    def __init__(self, dsFactory, maxBytes, maxTime, minTries=1):
        self.maxTime = maxTime
        self.dsFactoryMem = MemCheckDSFactory(dsFactory, maxBytes, self.memCallback)
        self.dsFactoryTime = TimeCheckDSFactory(dsFactory, maxTime, TimeoutError)
        self.algorithms = [BFS(self.dsFactoryMem), IDAstar(self.dsFactoryMem),
            BFS(self.dsFactoryTime), IDAstar(self.dsFactoryTime)]
        self.currAlgoIndex = AlgorithmPicker._IDAstar_TIME
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
            if isinstance(self.algorithms[self.currAlgoIndex], BFS):
                self.currAlgoIndex = AlgorithmPicker._IDAstar_TIME
                #self.fromBFS = True
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                return path
            elif isinstance(self.algorithms[self.currAlgoIndex], IDAstar):
                raise MemoryError

        except TimeoutError:
            if self.currAlgoIndex == AlgorithmPicker._IDAstar_TIME:
                #if not self.fromBFS or self.numTries > self.minTries:
                self.currAlgoIndex = AlgorithmPicker._BFS_MEM
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                #print(path)
                return path
            
    def memCallback(self):
        raise MemoryError


