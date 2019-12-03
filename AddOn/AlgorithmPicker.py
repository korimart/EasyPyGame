from AddOn.Algorithm import *
from AddOn.DSFactory import *
import multiprocessing
import time

class AlgorithmPicker:

    _BFS = 0
    _IDAstar = 1

    def __init__(self, dsFactory, maxBytes, maxTime, minTries=1):
        self.maxTime = maxTime
        self.dsFactory = TimeCheckDSFactory(MemCheckDSFactory(dsFactory, maxBytes, self.memCallback), maxTime, TimeoutError)
        self.algorithms = [BFS(self.dsFactory), IDAstar(self.dsFactory)]
        self.currAlgoIndex = AlgorithmPicker._BFS
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
            elif self.currAlgoIndex == AlgorithmPicker._IDAstar:
                raise MemoryError("self.currAlgoIndex == AlgorithmPicker._IDAstar:")

        except TimeoutError:
            if self.currAlgoIndex == AlgorithmPicker._IDAstar:
                #if not self.fromBFS or self.numTries > self.minTries:
                self.currAlgoIndex = AlgorithmPicker._BFS
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                #print(path)
                return path
            elif self.currAlgoIndex == AlgorithmPicker._BFS:
                raise TimeoutError("self.currAlgoIndex == AlgorithmPicker._BFS:")
            
    def memCallback(self):
        raise MemoryError


