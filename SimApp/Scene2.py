import EasyPygame
from EasyPygame.Components import *
from SimApp.Scene2StateContext import Scene2StateContext

class Scene2(Scene):
    def __init__(self):
        super().__init__()
        self.dataTuple = None
        self.stateContext = None

    def onLoad(self):
        self.stateContext = Scene2StateContext(self, *self.dataTuple)

    def setInputData(self, dataTuple):
        self.dataTuple = dataTuple

    def restart(self):
        self.clearGameObjects()
        self.stateContext = Scene2StateContext(self, *self.dataTuple)
        self.camera.reset()

    def postRender(self, ms):
        if EasyPygame.isDown("KP9"):
            self.camera.setDistanceDelta(0.01 * ms)
        if EasyPygame.isDown("KP7"):
            self.camera.setDistanceDelta(-0.01 * ms)
        if EasyPygame.isDown1stTime("KP5"):
            self.camera.setDistance(3)