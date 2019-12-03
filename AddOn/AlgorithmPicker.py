from AddOn.Algorithm import *
from AddOn.DSFactory import *
import multiprocessing
import time

class AlgorithmPicker:

    _BFS_INDEX = 0
    _IDAstar_INDEX = 1
    
    def __init__(self, dsFactory, maxBytes, maxTime, minTries):
        self.maxTime = maxTime
        self.dsFactory = MemCheckDSFactory(dsFactory, maxBytes, self.memCallback)
        self.algorithms = [BFS(self.dsFactory), IDAstar(self.dsFactory)]
        self.currAlgoIndex = 1
        self.fromBFS = False
        self.minTries = minTries
        self.numTries = 0

    def sol(self, ret, pointA, pointB, mmap):
        ret.put(self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap))

    def findPath(self, pointA, pointB, mmap):
        try:
            if self.currAlgoIndex == AlgorithmPicker._BFS_INDEX:
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                return path

            elif self.currAlgoIndex == AlgorithmPicker._IDAstar_INDEX:
                ret = multiprocessing.Queue()
                p = multiprocessing.Process(target=self.sol,
                name="findPath", args=(ret, pointA, pointB, mmap))
                p.start()
                p.join(self.maxTime)

                if p.is_alive():
                    if not self.fromBFS or self.numTries > self.minTries:
                        p.terminate()
                        p.join()
                        print('late')
                        self.currAlgoIndex = AlgorithmPicker._BFS_INDEX
                        path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                        print(path)
                        return path
                else:
                    p.join()
                    print("in time")
                    if self.fromBFS:
                        if self.numTries < self.minTries:
                            self.numTries += 1
                        elif self.numTries >= self.minTries:
                            self.fromBFS = False
                            self.numTries = 0
                    path = ret.get()
                    print(path)
                    return path
        
        except MemoryError:
            if isinstance(self.algorithms[self.currAlgoIndex], BFS):
                self.currAlgoIndex = AlgorithmPicker._IDAstar_INDEX
                self.fromBFS = True
                path = self.algorithms[self.currAlgoIndex].findPath(pointA, pointB, mmap)
                return path
            elif isinstance(self.algorithms[self.currAlgoIndex], IDAstar):
                raise MemoryError
            
    def memCallback(self):
        raise MemoryError


