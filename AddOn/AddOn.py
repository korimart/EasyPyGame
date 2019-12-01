import threading
from functools import partial

from AddOn.Algorithm import *
from AddOn.Behavior import *
from AddOn.DSFactory import *
from AddOn.Map import *

class AddOn:
    def __init__(self):
        self.mmap = None
        self.behavior = BehaviorGoFast()
        self.dsFactory = InsertCallbackDSFactory(DSFactory(), self._inserted)
        self.algorithm = BFS(self.dsFactory)
        self.pathFinder = VisitOrderProducer(self.algorithm)

        # test
        self.painter = Painter()
        self.paintingPF = PaintingPathFinder(self.pathFinder, self.painter)
        self.sim = None

    def go(self, robot):
        self.painter.sim = robot
        self.sim = robot
        self.behavior.go(robot, self.mmap, self.paintingPF)

    def setMap(self, size, hazardList, startingPoint, targetList):
        self.mmap = Map(size, hazardList, targetList, startingPoint)
        self.painter.size = size

    def _inserted(self, item):
        if type(item) is tuple:
            try:
                self.painter.draw(*item)
            except:
                return
        else:
            try:
                for pos in item:
                    self.painter.draw(*pos)
            except:
                return

class PaintingPathFinder:
    def __init__(self, pathFinder, painter):
        self.pathFinder = pathFinder
        self.painter = painter

    def findPath(self, startingPoint, targetList, mmap):
        self.painter.clear()
        path = self.pathFinder.findPath(startingPoint, targetList, mmap)
        self.painter.clear()
        for pos in path:
            self.painter.draw(*pos)
        self.painter.flush()
        return path

class Painter:
    def __init__(self):
        self.size = None
        self.array = None
        self.package = []
        self.sim = None

    def draw(self, x, y):
        if self.array[y][x] == 0:
            self.package.append((x, y))
        self.array[y][x] += 1

    def clear(self):
        self.flush()
        self.sim.clearColor()
        self.array = [[0 for _ in range(self.size[0])] for _ in range(self.size[1])]

    def flush(self):
        if self.package:
            self.sim.colorTileArray(self.package)
            self.package = []
