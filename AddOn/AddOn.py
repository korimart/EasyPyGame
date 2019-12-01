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
        self.algorithm = IDAstar(self.dsFactory)
        self.pathFinder = VisitOrderProducer(self.algorithm)

        # test
        self.painter = PathPainter(self.pathFinder)
        self.sim = None

    def go(self, robot):
        self.painter.SIMInterface = robot
        self.sim = robot
        self.behavior.go(robot, self.mmap, self.painter)

    def setMap(self, size, hazardList, startingPoint, targetList):
        self.mmap = Map(size, hazardList, targetList, startingPoint)

    def _inserted(self, item):
        self.sim.colorTile(*item)
        # print(item)

class PathPainter:
    def __init__(self, pathFinder):
        self.pathFinder = pathFinder
        self.SIMInterface = None

    def findPath(self, startingPoint, targetList, mmap):
        path = self.pathFinder.findPath(startingPoint, targetList, mmap)
        self.SIMInterface.clearColor()
        # for pos in path:
        #     self.SIMInterface.colorTile(*pos)
        return path