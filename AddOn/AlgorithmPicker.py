from AddOn.Algorithm import *
from AddOn.DSFactory import *
import multiprocessing
import time

class AlgorithmPicker:

    _BFS = 0
    _IDAstar = 1
    _BFS_MEM_ONLY = 2
    _IDAstar_MEM_ONLY = 3

    def __init__(self, dsFactory, maxBytes, maxTime, minTries=3):
        self.maxTime = maxTime
        self.maxBytes = maxBytes
        self.dsFactPaintOnly = dsFactory
        self.dsFactory = TimeCheckDSFactory(MemCheckDSFactory(dsFactory, self.maxBytes, self.memCallback), maxTime, TimeoutError)
        self.dsFactMemOnly = self.dsFactory.dsFactory
        self.algorithms = [BFS(self.dsFactory), IDAstar(self.dsFactory), BFS(self.dsFactMemOnly), IDAstar(self.dsFactMemOnly)]
        self.currAlgoIndex = AlgorithmPicker._BFS
        self.fromBFS = False
        self.minTries = minTries
        self.numTries = 0
        self.IDAsTimeout = False
        self.BFS_MemOut = False

    def findPath(self, pointA, pointB, mmap):
        try:
            if self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY:
                if self.minTries > self.numTries:
                    #print("self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY :: self.minTries > self.numTries")
                    #print("self.minTries, self.numTries :: ", self.minTries, self.numTries)
                    path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                    self.numTries += 1
                    return path
                elif self.minTries <= self.numTries:
                    print("self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY :: Enough Tries")
                    print("self.currAlgoIndex = AlgorithmPicker._IDAstar")
                    self.currAlgoIndex = AlgorithmPicker._IDAstar
                    path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                    self.numTries = 0
                    return path
            #print("self.currAlgoIndex ::", self.currAlgoIndex)
            else:
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                return path

        except MemoryError:
            if self.currAlgoIndex == AlgorithmPicker._BFS:
                print("MemoryError :: self.currAlgoIndex == AlgorithmPicker._BFS :: Trying IDA* MemOnly")
                print("without changing currAlgoIndex")
                path = IDAstar(MemCheckDSFactory(self.dsFactPaintOnly, self.maxBytes, self.memCallback)).findPath(pointA, pointB, mmap)
                return path
            elif self.currAlgoIndex == AlgorithmPicker._IDAstar:
                print("MemoryError :: self.currAlgoIndex == AlgorithmPicker._IDAstar :: Fatal. Nothing We Can Do About it.")
                raise MemoryError("self.currAlgoIndex == AlgorithmPicker._IDAstar:")
            elif self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY:
                print("MemoryError :: self.currAlgoIndex == AlgorithmPicker._BFS :: Trying IDA* MemOnly")
                print("without changing currAlgoIndex")
                path = IDAstar(MemCheckDSFactory(self.dsFactPaintOnly, self.maxBytes, self.memCallback)).findPath(pointA, pointB, mmap)
                return path
            #this actually cannot occur
            elif self.currAlgoIndex == AlgorithmPicker._IDAstar_MEM_ONLY:
                print("MemoryError :: self.currAlgoIndex == AlgorithmPicker._IDAstar_MEM_ONLY :: Fatal. Nothing We Can Do About it.")
                raise MemoryError("self.currAlgoIndex == AlgorithmPicker._IDAstar_MEM_ONLY:")

        except TimeoutError:
            if self.currAlgoIndex == AlgorithmPicker._IDAstar:
                #if not self.fromBFS or self.numTries > self.minTries:
                print("TimeoutError :: self.currAlgoIndex == AlgorithmPicker._IDAstar :: It will try BFS MemOnly", self.minTries, "times")
                print("self.currAlgoIndex = AlgorithmPicker._BFS_MEM_ONLY")
                self.currAlgoIndex = AlgorithmPicker._BFS_MEM_ONLY
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                self.numTries = 1
                return path
            # this can't happen
            elif self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY:
                if self.minTries > self.numTries:
                    print("TimeoutError :: self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY :: self.minTries > self.numTries")
                    path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                    self.numTries += 1
                    return path
                elif self.minTries <= self.numTries:
                    print("TimeoutError :: self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY :: self.minTries <= self.numTries")
                    print("self.currAlgoIndex = AlgorithmPicker._IDAstar")
                    self.currAlgoIndex = AlgorithmPicker._IDAstar
                    path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                    self.numTries = 0
                    return path
            elif self.currAlgoIndex == AlgorithmPicker._BFS:
                print("TimeoutError :: self.currAlgoIndex == AlgorithmPicker._BFS_ :: ")
                print("self.currAlgoIndex = AlgorithmPicker._IDAstar")
                self.currAlgoIndex = AlgorithmPicker._IDAstar
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                return path

                    
            
    def memCallback(self):
        raise MemoryError


