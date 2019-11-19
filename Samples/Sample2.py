import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame

class inputIdle(EasyPygame.Components.InputHandler):
    def update(self, gameObject, ms):
        for key in ["d", "a", "w", "s"]:
            if EasyPygame.isDown1stTime(key):
                gameObject.lastStateKey = None
                gameObject.currentKey = key
                gameObject.FSM.switchState(2, ms)
                break

class inputRunning(EasyPygame.Components.InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown(gameObject.currentKey):
            if gameObject.currentKey == "d":
                gameObject.rect.x += 0.1 * ms
            elif gameObject.currentKey == "a":
                gameObject.rect.x -= 0.1 * ms
            elif gameObject.currentKey == "w":
                gameObject.rect.y += 0.1 * ms
            elif gameObject.currentKey == "s":
                gameObject.rect.y -= 0.1 * ms
        else:
            gameObject.lastStateKey = gameObject.currentKey
            gameObject.currentKey = None
            gameObject.FSM.switchState(1, ms)


class Character(EasyPygame.Components.GameObject):
    def __init__(self, scene, name):
        super().__init__(scene, name)
        self.lastStateKey = None
        self.currentKey = None

class Scene1(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()
        self.character = None

    def onLoad(self):
        EasyPygame.load("animated.png")
        self.character = Character(self, "Character")
        self.character.addInputHandler(inputIdle())
        self.character.addInputHandler(inputRunning())
        for i in range(9):
            imageRect = EasyPygame.Rect((8 + i) * 16, 16, 16, 16)
            self.character.addTextureView(EasyPygame.Components.TextureView("animated.png", imageRect))

        self.character.FSM.addState(EasyPygame.Components.GameObjectState(1, 0, name="idle"))
        self.character.FSM.addState(EasyPygame.Components.GameObjectState(2, 0, name="running"))
        self.character.FSM.attachAnimationState(1, EasyPygame.Components.SpriteAnimState(1000, [1, 2, 3, 4]))
        self.character.FSM.attachAnimationState(2, EasyPygame.Components.SpriteAnimState(1000, [5, 6, 7, 8]))

        self.character.FSM.switchState(1, 0)

    def preRender(self, ms):
        EasyPygame.pprint("This is Scene1", 0, 0)

    def postRender(self, ms):
        if EasyPygame.isDown("KP9"):
            self.camera.setDistanceDelta(0.001 * ms)
        if EasyPygame.isDown("KP7"):
            self.camera.setDistanceDelta(-0.001 * ms)
        elif EasyPygame.isDown1stTime("KP5"):
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
