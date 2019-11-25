import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame
from EasyPygame.Components import *

class idle(GameObjectState):
    def __init__(self, key, otherKey, runIndex, otherRunIndex):
        super().__init__(0, -1)
        self.key = key
        self.otherKey = otherKey
        self.runIndex = runIndex
        self.otherRunIndex = otherRunIndex

    def update(self, gameObject, ms):
        for key in [self.key, "s", "w"]:
            if EasyPygame.isDown(key):
                gameObject.FSM.switchState(self.runIndex, ms)
        if EasyPygame.isDown(self.otherKey):
            gameObject.FSM.switchState(self.otherRunIndex, ms)

class run(GameObjectState):
    DELTA = {
        "w" : (0, 0.01),
        "a" : (-0.01, 0),
        "s" : (0, -0.01),
        "d" : (0.01, 0)
    }
    def __init__(self, key, otherKey, idleIndex, otherRunIndex):
        super().__init__(0, -1)
        self.key = key
        self.otherKey = otherKey
        self.idleIndex = idleIndex
        self.otherRunIndex = otherRunIndex

    def update(self, gameObject, ms):
        isIdle = True
        for key in [self.key, "s", "w"]:
            if EasyPygame.isDown(key):
                gameObject.rect.x += self.DELTA[key][0] * ms
                gameObject.rect.y += self.DELTA[key][1] * ms
                isIdle = False

        if isIdle:
            gameObject.FSM.switchState(self.idleIndex, ms)
        if EasyPygame.isDown(self.otherKey):
            gameObject.FSM.switchState(self.otherRunIndex, ms)

class Scene1(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()
        self.character = None

    def onLoad(self):
        for i in range(4):
            EasyPygame.load("elf_f_idle_anim_f" + str(i) + ".png")
            EasyPygame.load("elf_f_run_anim_f" + str(i) + ".png")

        self.characters = []
        for j in range(3):
            character = GameObject(self, "Character")

            for i in range(4):
                imageRect = EasyPygame.Rect(0, 0.25, 1, 0.75)
                character.addTextureView(TextureView("elf_f_idle_anim_f" + str(i) + ".png", \
                    imageRect, flipX=True))

            for i in range(4):
                imageRect = EasyPygame.Rect(0, 0.25, 1, 0.75)
                character.addTextureView(TextureView("elf_f_run_anim_f" + str(i) + ".png", imageRect, \
                    flipX=True))

            for i in range(4):
                imageRect = EasyPygame.Rect(0, 0.25, 1, 0.75)
                character.addTextureView(TextureView("elf_f_idle_anim_f" + str(i) + ".png", \
                    imageRect))

            for i in range(4):
                imageRect = EasyPygame.Rect(0, 0.25, 1, 0.75)
                character.addTextureView(TextureView("elf_f_run_anim_f" + str(i) + ".png", imageRect))

            # 1: leftIdle, 2: leftRun, 3:rightIdle, 4:rightRun
            character.FSM.addState(idle("a", "d", 2, 4))
            character.FSM.addState(run("a", "d", 1, 4))
            character.FSM.addState(idle("d", "a", 4, 2))
            character.FSM.addState(run("d", "a", 3, 2))

            # 1234leftIdle, 5678leftRun, 9101112rightIdle, 13141516rightRun
            character.FSM.attachConcurrentState(1, SpriteAnimState(500, [1, 2, 3, 4]))
            character.FSM.attachConcurrentState(2, SpriteAnimState(250, [5, 6, 7, 8]))
            character.FSM.attachConcurrentState(3, SpriteAnimState(500, [9, 10, 11, 12]))
            character.FSM.attachConcurrentState(4, SpriteAnimState(250, [13, 14, 15, 16]))

            character.FSM.switchState(1, 0)
            character.rect.x = j
            self.characters.append(character)

    def preRender(self, ms):
        EasyPygame.pprint("This is Scene1", 0, 0)

    def postRender(self, ms):
        if EasyPygame.isDown("KP9"):
            self.camera.setDistanceDelta(0.005 * ms)
        if EasyPygame.isDown("KP7"):
            self.camera.setDistanceDelta(-0.005 * ms)
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

    def onUnLoad(self):
        for i in range(4):
            EasyPygame.unLoad("elf_f_idle_anim_f" + str(i) + ".png")
            EasyPygame.unLoad("elf_f_run_anim_f" + str(i) + ".png")


if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()
