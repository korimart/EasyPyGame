import os
import sys
THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
import EasyPygame
#os.chdir(THISDIR)
from SimApp import Robot, RobotForDebug
from AddOn import *


class Scene1(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()
  

if __name__ == "__main__":
    hazards = [(1, 0), (1, 1), (1, 3)]
    size = (3, 4)
    searchPoints = [(2, 0), (0, 3)]
    robotLocation = (0, 0)

    
    
    map = Map(hazards = hazards, size=size, searchPoints=searchPoints,
        robot=(0,0))
    
    pf = bfsShortestFirst()
    print(pf.adaptiveShortestFirst(map.minPoints, map.size, map.hazards, map.robot,
        map.searchPoints, pf.adaptiveBfs, 10000))
    print(pf.findPath(map, (0, 0)))

    robotdebug = RobotForDebug.RobotForDebug(map, scene=Scene1())
    addon = AddOn(hazards = hazards, size=size, searchPoints=searchPoints,
        robot=robotLocation)
    addon.go(robot=robotdebug)
    print(addon.map.pathTaken, robotdebug.position)

    
    


