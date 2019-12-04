from AddOn.Algorithm import *
from AddOn.DSFactory import *
import multiprocessing
import time

class AlgorithmPicker:

    _BFS = 0
    _IDAstar = 1
    _BFS_MEM_ONLY = 2
    _IDAstar_MEM_ONLY = 3

    def __init__(self, painter, dsFactory, maxBytes, maxTime, minTriesTime=3, minTriesMem=1):
        self.painter = painter
        self.maxTime = maxTime
        self.maxBytes = maxBytes
        self.dsFactory = TimeCheckDSFactory(MemCheckDSFactory(dsFactory, self.maxBytes, self.memCallback), maxTime, TimeoutError)
        self.dsFactMemOnly = MemCheckDSFactory(dsFactory, self.maxBytes, self.memCallback)
        self.algorithms = [BFS(self.dsFactory), IDAstar(self.dsFactory), BFS(self.dsFactMemOnly), IDAstar(self.dsFactMemOnly)]
        self.currAlgoIndex = AlgorithmPicker._BFS
        self.memExceptionfromBFS = False
        self.minTriesTime = minTriesTime
        self.numTriesTime = 0
        self.minTriesMem = minTriesMem
        self.numTriesMem = 0

    def findPath(self, pointA, pointB, mmap):
        path = self._findPath(pointA, pointB, mmap)
        self.painter.clear()
        for coord in path:
            self.painter.draw(*coord)
        return path

    def _findPath(self, pointA, pointB, mmap):
        while(True):
            try:
                print("self.currAlgoIndex :: Before findPath Call::", self.currAlgoIndex)
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                print("self.currAlgoIndex :: After findPath Call::", self.currAlgoIndex)
                if self.currAlgoIndex == AlgorithmPicker._IDAstar_MEM_ONLY:
                    if self.minTriesMem > self.numTriesMem:
                        self.numTriesMem += 1
                        print("self.currAlgoIndex == AlgorithmPicker._IDAstar_MEM_ONLY :: Trying IDA*: ", self.numTriesMem)
                        print("self.minTriesMem, self.numTriesMem :: ", self.minTriesMem, self.numTriesMem)
                        if self.minTriesMem <= self.numTriesMem:
                            self.numTriesMem = 0
                            print("self.currAlgoIndex == AlgorithmPicker._IDAstar_MEM_ONLY :: Enough Tries")
                            if self.memExceptionfromBFS:
                                self.currAlgoIndex = AlgorithmPicker._BFS
                                print("self.currAlgoIndex = AlgorithmPicker.AlgorithmPicker._BFS")
                            else:
                                self.currAlgoIndex = AlgorithmPicker._BFS_MEM_ONLY
                                print("self.currAlgoIndex = AlgorithmPicker.AlgorithmPicker._BFS_MEM_ONLY")
                
                # Note:
                # If MEMORY ERROR OCCURS WHEN self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY,
                # self.currAlgoIndex CHANGES TO _IDAstar_MEM_ONLY
                # WHEN IT COMES BACK TO _BFS_MEM_ONLY, self.numTriesTime += 1 WILL BE PERFORMED
                # EVEN THOUGH IT WANSN"T BFS WHO FOUND THE PATH(S)

                if self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY:
                    if self.minTriesTime > self.numTriesTime:
                        self.numTriesTime += 1
                        print("self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY :: Trying BFS: ", self.numTriesTime)
                        print("self.minTriesTime, self.numTriesTime :: ", self.minTriesTime, self.numTriesTime)
                        if self.minTriesTime <= self.numTriesTime:
                            self.numTriesTime = 0
                            print("self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY :: Enough Tries")
                            print("self.currAlgoIndex = AlgorithmPicker._IDAstar")
                            self.currAlgoIndex = AlgorithmPicker._IDAstar
                
                return path

            except MemoryError:
                if self.currAlgoIndex == AlgorithmPicker._BFS:
                    print("MemoryError :: self.currAlgoIndex == AlgorithmPicker._BFS :: Trying IDA* MemOnly")
                    print("without changing currAlgoIndex")
                    self.currAlgoIndex = AlgorithmPicker._IDAstar_MEM_ONLY
                    self.MemExceptionFromBFS = True
                elif self.currAlgoIndex == AlgorithmPicker._IDAstar:
                    print("MemoryError :: self.currAlgoIndex == AlgorithmPicker._IDAstar :: Fatal. Nothing We Can Do About it.")
                    return
                elif self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY:
                    print("MemoryError :: self.currAlgoIndex == AlgorithmPicker._BFS :: Trying IDA* MemOnly")
                    self.currAlgoIndex = AlgorithmPicker._IDAstar_MEM_ONLY
                    self.MemExceptionFromBFS = False
                elif self.currAlgoIndex == AlgorithmPicker._IDAstar_MEM_ONLY:
                    print("MemoryError :: self.currAlgoIndex == AlgorithmPicker._IDAstar_MEM_ONLY :: Fatal. Nothing We Can Do About it.")
                    return

            except TimeoutError:
                if self.currAlgoIndex == AlgorithmPicker._IDAstar:
                    #if not self.fromBFS or self.numTries > self.minTries:
                    print("TimeoutError :: self.currAlgoIndex == AlgorithmPicker._IDAstar :: It will try BFS MemOnly", self.minTriesTime, "times")
                    print("self.currAlgoIndex = AlgorithmPicker._BFS_MEM_ONLY")
                    self.currAlgoIndex = AlgorithmPicker._BFS_MEM_ONLY
                    self.numTriesTime = 0
                elif self.currAlgoIndex == AlgorithmPicker._BFS:
                    print("TimeoutError :: self.currAlgoIndex == AlgorithmPicker._BFS_ :: ")
                    print("self.currAlgoIndex = AlgorithmPicker._IDAstar")
                    self.currAlgoIndex = AlgorithmPicker._IDAstar
            
    def memCallback(self):
        raise MemoryError


