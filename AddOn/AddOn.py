from AddOn.Algorithm import *
from AddOn.Behavior import *
from AddOn.DSFactory import *
from AddOn.Map import *

class AddOn:
    def __init__(self):
        self.mmap = None
        self.behavior = BehaviorGoFast()
        self.dsFactory = DSFactory()
        self.algorithm = IDAstar(self.dsFactory)
        self.pathFinder = VisitOrderProducer(self.algorithm)

        # test
        self.painter = PathFinder()

    def go(self, robot):
        self.painter.pathFinder = self.pathFinder
        self.painter.robot = robot
        self.behavior.go(robot, self.mmap, self.painter)

    def setMap(self, size, hazardList, startingPoint, targetList):
        self.mmap = Map(size, hazardList, targetList, startingPoint)

# test
class PathFinder:
    def __init__(self):
        self.pathFinder = None
        self.robot = None

    def findPath(self, startingPoint, targetList, mmap):
        path = self.pathFinder.findPath(startingPoint, targetList, mmap)
        robot.clearColor()
        for pos in path:
            robot.colorTile(*pos)
        return path