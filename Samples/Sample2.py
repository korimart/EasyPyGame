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
        for i in range(4):
            EasyPygame.load("elf_f_idle_anim_f" + str(i) + ".png")
            EasyPygame.load("elf_f_run_anim_f" + str(i) + ".png")

        self.characters = []
        for j in range(100):
            character = GameObject(self, "Character")
            character.addInputHandler(characterInput())
            character.useInputHandler(1)

            for i in range(4):
                imageRect = EasyPygame.Rect(0, 12, 16, 16)
                character.addTextureView(TextureView("elf_f_idle_anim_f" + str(i) + ".png", imageRect, fitObject=False, crop=True, scale=(10, 10)))

            for i in range(4):
                imageRect = EasyPygame.Rect(0, 12, 16, 16)
                character.addTextureView(TextureView("elf_f_run_anim_f" + str(i) + ".png", imageRect))

            character.FSM.addState(SpriteAnimState(500, [1, 2, 3, 4]))
            character.FSM.addState(SpriteAnimState(500, [5, 6, 7, 8]))

            character.FSM.switchState(1, 0)
            character.rect.x = 100 * j
            self.characters.append(character)

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
        for i in range(4):
            EasyPygame.unLoad("elf_f_idle_anim_f" + str(i) + ".png")
            EasyPygame.unLoad("elf_f_run_anim_f" + str(i) + ".png")


if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()
