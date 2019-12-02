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
        self.testObj1 = None
        self.testObj2 = None

    def onLoad(self):
        EasyPygame.load("Carrot.jpg")
        EasyPygame.load("darkness.png")
        self.carrot = GameObject(self, "Carrot")
        self.carrot.addTextureView(TextureView("Carrot.jpg"))
        self.carrot.useTextureView(1)

        self.testObj1 = EasyPygame.Components.GameObject(self, "Test1")
        self.testObj1.addTextureView(TextureView("darkness.png", EasyPygame.Rect(0, 0, 1/4, 1/4), blending=True))
        self.testObj1.useTextureView(1)
        self.testObj1.rect.x = -1
        self.testObj1.rect.y = -1
        self.testObj1.rect.z = -1

        self.testObj2 = GameObject(self, "Test2")
        self.testObj2.addTextureView(DefaultTextureView((1, 0, 0)))
        self.testObj2.useTextureView(1)
        self.testObj2.rect.x = -1
        self.testObj2.rect.y = -2
        self.testObj2.rect.width = 2
        self.testObj2.rect.z = 1

        self.button = GUI.Button(self, "Button", lambda: self.testCallback())
        self.button.rect.x = 2
        self.button.rect.y = -2

    def preRender(self, ms):
        EasyPygame.pprint("This is Scene1", 0, 0)

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

    def testCallback(self):
        print("haha")

class Scene2(Scene):
    def __init__(self):
        super().__init__()

    def onLoad(self):
        self.obj1 = GameObject(self, "obj1")
        self.obj1.addTextureView(DefaultTextureView((1, 0, 0)))

        # first parameter is gameObjectStateIndex to attach state to.
        # second parameter is an concurrent state
        # first parameter of the constructor is duration in miliseconds of the animation from start to end
        # second parameter is a list of textureViewIndices of animation
        # in this case, animates between textureView 0 and 1 each with duration of 0.5 seconds and total of 1 second
        self.obj1.FSM.attachConcurrentState(0, SpriteAnimState(100, [0, 1]))

        self.textbox = GUI.TextBox(self, "textbox1", "ab")
        self.textbox.rect.x = 0
        self.textbox.rect.y = 1
        self.textbox.setWidth(4)

    def postRender(self, ms):
        EasyPygame.pprint("This is Scene2", 0, 0)

        if EasyPygame.isDown1stTime("KP1"):
            EasyPygame.consume("KP1")
            EasyPygame.nextScene("Scene2", "Scene1")
        if EasyPygame.isDown("KP9"):
            self.camera.setDistanceDelta(0.001 * ms)
        if EasyPygame.isDown("KP7"):
            self.camera.setDistanceDelta(-0.001 * ms)
        if EasyPygame.isDown1stTime("KP5"):
            self.camera.setDistance(1)
            self.camera.moveTo(0, 0)
        if EasyPygame.isDown("KP4"):
            self.camera.move((-0.01 * ms, 0))
        if EasyPygame.isDown("KP8"):
            self.camera.move((0, 0.01 * ms))
        if EasyPygame.isDown("KP6"):
            self.camera.move((0.01 * ms, 0))
        if EasyPygame.isDown("KP2"):
            self.camera.move((0, -0.01 * ms))

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()
