import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame

class carrotHandler(EasyPygame.Components.InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("d"):
            gameObject.rect.x += 100
        elif EasyPygame.isDown1stTime("a"):
            gameObject.rect.x -= 100
        elif EasyPygame.isDown1stTime("w"):
            gameObject.rect.y += 100
        elif EasyPygame.isDown1stTime("s"):
            gameObject.rect.y -= 100
        elif EasyPygame.isDown1stTime("p"):
            EasyPygame.loadScene("Scene2")
            EasyPygame.switchScene("Scene2")
            EasyPygame.unloadScene("Scene1")

class Scene1(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()
        self.carrot = None
        self.testObj1 = None
        self.testObj2 = None

    def load(self):
        EasyPygame.load("Carrot.jpg")
        self.carrot = EasyPygame.Components.GameObject(self, "Carrot")
        self.carrot.textureView = EasyPygame.Components.TextureView("Carrot.jpg")
        self.carrot.inputHandler = carrotHandler()

        self.testObj1 = EasyPygame.Components.GameObject(self, "Test1")
        self.testObj1.rect.x = 100
        self.testObj1.z = -1

        self.testObj2 = EasyPygame.Components.GameObject(self, "Test2")
        self.testObj2.rect.x = -150
        self.testObj2.rect.y = -150
        self.testObj2.rect.width = 200
        self.testObj2.z = 1

    def preRender(self):
        EasyPygame.pprint("preRender preRender preRender", 0, 0)

    def postRender(self):
        EasyPygame.pprint("postRender postRender postRender", 0, 100)

    def unload(self):
        EasyPygame.unload("abc.jpg")

class Scene2(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()

    def postRender(self):
        EasyPygame.pprint("this is scene2", 0, 0)

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()
