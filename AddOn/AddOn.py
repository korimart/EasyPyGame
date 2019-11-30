from AddOn.Algorithm import *
from AddOn.Behavior import *
from AddOn.DSFactory import *
from AddOn.Map import *

class AddOn:
    def __init__(self, hazards):
        self.mmap = Map((50, 50), hazards, [(19, 19)], (0, 0))
        self.behavior = BehaviorGoFast()
        self.dsFactory = DSFactory()
        self.algorithm = BFS(self.dsFactory)
        self.visitOrder = VisitOrderProducer(self.algorithm)

    def go(self, robot):
        self.behavior.go(robot, self.mmap, self.visitOrder)