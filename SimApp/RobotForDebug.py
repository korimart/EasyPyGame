import os
import sys
THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
import EasyPygame
#os.chdir(THISDIR)
from SimApp import Robot
import AddOn

class RobotForDebug(Robot.Robot):
    def __init__(self, map, scene=None, rect=(0, 0), position=[0, 0, 0], name='Robot',
        increment=100, errorRate=0.05, delay = 0):
        super().__init__(scene=scene, rect=(0, 0), position=[0, 0, 0], name='Robot',
        increment=100, errorRate=0.05, delay = 0)
        self.map = map
        self.MaybeIShouldHavePutThisMethodInMap = AddOn.GoSlow(self.map).calculateCoordinates
        self.MaybeIShouldHavePutThisMethodInMap2 = AddOn.GoSlow(self.map).sanityCheck

    def move(self):
        loc = self.location()
        super().move()
        if not self.MaybeIShouldHavePutThisMethodInMap2(self.map.minPoints,
            self.map.size, self.location()):
            self.setLocation(loc)
        
            


    def senseHazard(self):
        if tuple(self.MaybeIShouldHavePutThisMethodInMap(
            self.location(), self.direction())) in self.map.hazards:
            return True
        else:
            return False
    
    def senseBlob(self):
        d = self.direction()
        blobsIndicator = []
        for i in range(4):
            if tuple(self.MaybeIShouldHavePutThisMethodInMap(
                self.location(), d)) in self.map.searchPoints:
                blobsIndicator.append(True)
            else:
                blobsIndicator.append(False)
            d = (d + 1) % 4
        return blobsIndicator



