import EasyPygame
from EasyPygame.Components import *
from SimApp.Scene2StateContext import Scene2StateContext

class Scene2(Scene):
    def __init__(self):
        super().__init__()
        self.dataTuple = None
        self.stateContext = None

    def onLoad(self):
        EasyPygame.load("animated.png")
        EasyPygame.load("arrow.png")
        self.stateContext = Scene2StateContext(self, *self.dataTuple)

    def onUnLoad(self):
        EasyPygame.unLoad("animated.png")
        EasyPygame.unLoad("arrow.png")

    def setInputData(self, dataTuple):
        self.dataTuple = dataTuple

    def restart(self):
        self.clearGameObjects()
        self.stateContext = Scene2StateContext(self, *self.dataTuple)
        self.camera.reset()