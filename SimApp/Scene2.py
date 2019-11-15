import os, sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))

import EasyPygame

class Scene2(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()
        self.width = 10
        self.height = 10
        self.startPos = (0, 0)
        self.targetPosList = [[9, 9]]
        self.knownHazardsList = [[4, 4]]

    def onLoad(self):
        pass

    def setInputData(self, width, height, startPos, targetPosList, knownHazardsList):
        self.width = width
        self.height = height
        self.startPos = startPos
        self.targetPosList = targetPosList
        self.knownHazardsList = knownHazardsList

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene2")
    EasyPygame.switchScene("Scene2")
    EasyPygame.run()