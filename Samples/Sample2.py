import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame
from EasyPygame.Components import *

class characterInput(EasyPygame.Components.InputHandler):
    def update(self, gameObject, ms):
        wasPressed = False
        if EasyPygame.isDown("d"):
            gameObject.rect.x += int(0.1 * ms)
            wasPressed = True
        if EasyPygame.isDown("a"):
            prev = gameObject.rect.x
            gameObject.rect.x -= int(0.1 * ms)
            wasPressed = True
        if EasyPygame.isDown("w"):
            gameObject.rect.y += int(0.1 * ms)
            wasPressed = True
        if EasyPygame.isDown("s"):
            gameObject.rect.y -= int(0.1 * ms)
            wasPressed = True
        
        if wasPressed:
            if gameObject.FSM.currentStateIndex != 2:
                gameObject.FSM.switchState(2, ms)
        else:
            if gameObject.FSM.currentStateIndex != 1:
                gameObject.FSM.switchState(1, ms)
        
class Scene1(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()
        self.character = None

    def onLoad(self):
        EasyPygame.load("animated.png")
        self.character = GameObject(self, "Character")
        self.character.addInputHandler(characterInput())
        self.character.useInputHandler(1)
        # self.character.addTextureView(DefaultTextureView())
        # self.character.addTextureView(DefaultTextureView((255, 0, 0)))

        for i in range(9):
            imageRect = EasyPygame.Rect((8 + i) * 16, 16, 16, 16)
            self.character.addTextureView(TextureView("animated.png", None, fitObject=False, crop=True))

        self.character.FSM.addState(SpriteAnimState(1000, [1, 2, 3, 4]))
        self.character.FSM.addState(SpriteAnimState(1000, [5, 6, 7, 8]))
        # self.character.FSM.addState(GameObjectState(1, 1))
        # self.character.FSM.addState(GameObjectState(1, 2))

        self.character.FSM.switchState(1, 0)

    def preRender(self, ms):
        EasyPygame.pprint("This is Scene1", 0, 0)

    def postRender(self, ms):
        if EasyPygame.isDown("KP9"):
            self.camera.setDistanceDelta(0.001 * ms)
        if EasyPygame.isDown("KP7"):
            self.camera.setDistanceDelta(-0.001 * ms)
        if EasyPygame.isDown1stTime("KP5"):
            self.camera.setDistance(1)
            self.camera.moveTo(0, 0)
        if EasyPygame.isDown("KP4"):
            self.camera.move((-0.1 * ms, 0))
        if EasyPygame.isDown("KP8"):
            self.camera.move((0, 0.1 * ms))
        if EasyPygame.isDown("KP6"):
            self.camera.move((0.1 * ms, 0))
        if EasyPygame.isDown("KP2"):
            self.camera.move((0, -0.1 * ms))

    def onUnLoad(self):
        EasyPygame.unload("animated.png")

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()
