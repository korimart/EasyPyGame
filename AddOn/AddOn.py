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

    def go(self, robot):
        self.behavior.go(robot, self.mmap, self.pathFinder)

    def setMap(self, size, hazardList, startingPoint, targetList):
        self.mmap = Map(size, hazardList, targetList, startingPoint)