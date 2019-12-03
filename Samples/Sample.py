import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame
from EasyPygame.Components import *
from OpenGL.GL import *

class Scene1(Scene):
    def __init__(self):
        super().__init__()
        self.carrot = None
        self.button = None

    def onLoad(self):
        EasyPygame.load("Carrot.jpg")
        EasyPygame.load("darkness.png")
        self.carrot = GameObject(self, "Carrot")
        # ins1 = self.carrot.transform.copy()
        # ins1.rotate(25)
        # ins1.translate(1, 0, 0)
        # instances = [self.carrot.transform, ins1]
        # self.carrot.renderComp = TextureRenderComponent("Carrot.jpg")
        # self.carrot.renderComp = DefaultInstancedRenderComponent(instances)
        # self.carrot.renderComp = TextureInstancedRenderComponent(instances, "Carrot.jpg")
        self.carrot.renderComp = AnimationRenderComponent([TextureRenderComponent("Carrot.jpg"), \
            DefaultRenderComponent()], 500)

        self.button = GUI.Button(self, callback=self.testCallback)
        self.button.transform.translate(1, 0, 0)

    def testCallback(self):
        print("yes")

    def postRender(self, ms):
        if EasyPygame.isDown1stTime("RETURN"):
            EasyPygame.consume("RETURN")
            EasyPygame.nextScene("Scene1", "Scene2")
        if EasyPygame.isDown("KP9"):
            self.camera.setDistanceDelta(0.005 * ms)
        if EasyPygame.isDown("KP7"):
            self.camera.setDistanceDelta(-0.005 * ms)
        if EasyPygame.isDown1stTime("KP5"):
            self.camera.reset()
        if EasyPygame.isDown("KP4"):
            self.camera.move((-0.01 * ms, 0))
        if EasyPygame.isDown("KP8"):
            self.camera.move((0, 0.01 * ms))
        if EasyPygame.isDown("KP6"):
            self.camera.move((0.01 * ms, 0))
        if EasyPygame.isDown("KP2"):
            self.camera.move((0, -0.01 * ms))

    def onUnLoad(self):
        EasyPygame.unload("Carrot.jpg")

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()
