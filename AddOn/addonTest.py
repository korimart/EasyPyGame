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
    hazards = [(1, 4), (2, 2), (2, 3), (3, 4), (4, 3), (4, 2), (5, 1)]
    size = (6, 7)
    searchPoints = [(3, 2), (3, 3), (3, 6), (5, 4), (5, 0)]
    robotLocation = (1, 2)
    robotPosition = list(robotLocation)
    robotPosition.append(0)
    
    hazardsForSim = hazards.copy()
    hazardsForSim += [(1, 5), (2, 1), (1, 3)]
    searchPointsForSim = searchPoints.copy()
    searchPointsForSim += [(2, 1), (2, 5), (4, 0), (4, 2), (4, 4)]
   
    map = Map(hazards = hazards, size=size, searchPoints=searchPoints,
        robotLocation=robotLocation)
    mapForSim = Map(hazards = hazardsForSim, size=size, searchPoints=searchPointsForSim,
        robotLocation=robotLocation)
    
    
    pf = IDA_starShortestFirst()
    #pf = bfsShortestFirst()
    pa = PathAlgorithm()

    """
    #pa.possiblePositions(map.minPoints, map.size, map.hazards, (1,1))
    print(pa.bfs(map.minPoints, map.size, map.hazards,
       map.robotLocation, searchPoints[0]))
    print(pa.IDA_star(mapForSim.minPoints, mapForSim.size, mapForSim.hazards,
       (5,0), (5,4)))
    
    
    print(pf.pathFinder.adaptiveShortestFirst(map.minPoints, map.size, map.hazards,
       map.robotLocation, map.searchPoints.copy(), pf.pathFinder.adaptiveIDA_star, 1000000))
    print("IDAS: ", pf.pathFinder.shortestFirst(map.minPoints, map.size, map.hazards,
       map.robotLocation, map.searchPoints.copy(), pf.pathFinder.IDA_star))
    print(pf.findPath(map, robotLocation))
    """

    adapGoSlowIDAS = AdaptiveGoSlow(memoryThreshold=10000, timeThreshold=0.001,
        pathFinder=AdaptiveBfsShortestFirst(100000))

    robotdebug = RobotForDebug.RobotForDebug(mapForSim, scene=Scene1(),
        position=robotPosition, errorRate=0)
    addon = AddOn(hazards = hazards, size=size, searchPoints=searchPoints,
        robotLocation=robotLocation, behavior=adapGoSlowIDAS)
    addon.go(robot=robotdebug)
    print("Path Taken :: ", addon.map.pathTaken)
    print("Robot Position :: ", robotdebug.position)
    print("Blobs Found :: ", addon.map.blobs)
    print(set(searchPoints) <= addon.map.blobs <= set(searchPointsForSim))
