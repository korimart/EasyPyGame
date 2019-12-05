from AddOn.Algorithm import *
from AddOn.DSFactory import *
import multiprocessing
import time

class AlgorithmPicker:

    _BFS = 0
    _IDAstar = 1

    def __init__(self, painter, dsFactory, maxBytes, maxTime, minTriesTime=3, minTriesMem=1):
        self.painter = painter
        self.maxTime = maxTime
        self.maxBytes = maxBytes
        self.dsFactoryBoth = TimeCheckDSFactory(MemCheckDSFactory(dsFactory, self.maxBytes, self.memCallback), maxTime, TimeoutError)
        self.dsFactMemOnly = MemCheckDSFactory(dsFactory, self.maxBytes, self.memCallback)
        self.algorithms = [BFS(self.dsFactoryBoth), IDAstar(self.dsFactoryBoth)]
        self.currAlgoIndex = AlgorithmPicker._BFS
        self.minTriesTime = minTriesTime
        self.numTriesTime = 0
        self.minTriesMem = minTriesMem
        self.numTriesMem = 0
        self.memExceptionFromBFS = None

    def findPath(self, pointA, pointB, mmap):
        path = self._findPath(pointA, pointB, mmap)
        self.painter.clear()
        for coord in path:
            self.painter.draw(*coord)
        return path

    def _findPath(self, pointA, pointB, mmap):
        while(True):
            try:
                #print("self.currAlgoIndex and memOnly :: Before findPath Call::", self.currAlgoIndex)
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                #print("self.currAlgoIndex and memOnly :: After findPath Call::", self.currAlgoIndex)
                if (self.currAlgoIndex == AlgorithmPicker._IDAstar and
                    self.algorithms[self.currAlgoIndex].dsFactory == self.dsFactMemOnly):
                    if self.minTriesMem > self.numTriesMem:
                        self.numTriesMem += 1
                        print("Trying IDA* mem only :: minTriesMem, numTriesMem :: ", self.minTriesMem, self.numTriesMem)
                        if self.minTriesMem <= self.numTriesMem:
                            self.numTriesMem = 0
                            if self.memExceptionFromBFS:
                                self.currAlgoIndex = AlgorithmPicker._BFS
                                self.algorithms[self.currAlgoIndex].dsFactory = self.dsFactoryBoth                            
                                print("IDA* MemOnly :: Enough Tries :: IDA* MemOnly -> BFS")
                            else:
                                self.currAlgoIndex = AlgorithmPicker._BFS
                                self.algorithms[self.currAlgoIndex].dsFactory = self.dsFactMemOnly
                                print("IDA* MemOnly :: Enough Tries :: IDA* MemOnly -> BFS MemOnly")
                # Note:
                # IF MEMORY ERROR OCCURS WHEN self.currAlgoIndex == AlgorithmPicker._BFS_MEM_ONLY,
                # self.currAlgoIndex CHANGES TO _IDAstar_MEM_ONLY
                # WHEN IT COMES BACK TO _BFS_MEM_ONLY, self.numTriesTime += 1 WILL BE PERFORMED
                # EVEN THOUGH IT WANSN'T BFS WHO FOUND THE PATH(S)

                if (self.currAlgoIndex == AlgorithmPicker._BFS and
                    self.algorithms[self.currAlgoIndex].dsFactory == self.dsFactMemOnly):
                    if self.minTriesTime > self.numTriesTime:
                        self.numTriesTime += 1
                        print("Trying BFS mem only ", "self.minTriesTime, self.numTriesTime :: ", self.minTriesTime, self.numTriesTime)
                        if self.minTriesTime <= self.numTriesTime:
                            self.numTriesTime = 0
                            print("BFS MemOnly :: Enough Tries :: BFS MemOnly -> IDA*")
                            self.currAlgoIndex = AlgorithmPicker._IDAstar
                            self.algorithms[self.currAlgoIndex].dsFactory = self.dsFactoryBoth
                return path
            
            except MemoryError:
                if (self.currAlgoIndex == AlgorithmPicker._BFS and 
                    self.algorithms[self.currAlgoIndex].dsFactory == self.dsFactoryBoth):
                    print("MemoryError :: BFS -> IDA* Mem Only. It will try IDA* MemOnly", self.minTriesMem, "times")
                    self.currAlgoIndex = AlgorithmPicker._IDAstar
                    self.algorithms[self.currAlgoIndex].dsFactory = self.dsFactMemOnly
                    self.memExceptionFromBFS = True
                elif (self.currAlgoIndex == AlgorithmPicker._BFS and
                    self.algorithms[self.currAlgoIndex].dsFactory == self.dsFactMemOnly):
                    print("MemoryError :: BFS Mem Only -> IDA* Mem Only. It will try IDA* MemOnly", self.minTriesMem, "times")
                    self.currAlgoIndex = AlgorithmPicker._IDAstar
                    self.algorithms[self.currAlgoIndex].dsFactory = self.dsFactMemOnly
                    self.memExceptionFromBFS = False
                elif self.currAlgoIndex == AlgorithmPicker._IDAstar:
                    print("MemoryError :: IDA* :: Fatal. Nothing We Can Do About it.")
                    raise
                
            except TimeoutError:
                if self.currAlgoIndex == AlgorithmPicker._IDAstar:
                    print("TimeoutError :: IDA* -> BFS MemOnly. It will try BFS MemOnly", self.minTriesTime, "times")
                    self.currAlgoIndex = AlgorithmPicker._BFS
                    self.algorithms[self.currAlgoIndex].dsFactory = self.dsFactMemOnly
                    self.numTriesTime = 0
                elif self.currAlgoIndex == AlgorithmPicker._BFS:
                    print("TimeoutError :: BFS -> IDA* ")
                    self.currAlgoIndex = AlgorithmPicker._IDAstar
                    self.algorithms[self.currAlgoIndex].dsFactory = self.dsFactoryBoth
            
    def memCallback(self):
        raise MemoryError


