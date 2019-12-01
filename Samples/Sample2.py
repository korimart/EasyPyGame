import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame
from EasyPygame.Components import *
from SimApp.Floor import *
from SimApp.SkinChanger import *
from SimApp.Robot import *
from AddOn.Map import *
from AddOn.Behavior import *
from AddOn.Algorithm import *
from AddOn.DSFactory import *

class idle(GameObjectState):
    def __init__(self, key, otherKey, runIndex, otherRunIndex):
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
                gameObject.scene.camera.moveTo(gameObject.rect.x, gameObject.rect.y)
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
        EasyPygame.load("animated.png")

        # self.characters = []

        # self.tileMap = GameObject(self, "TileMap")
        # self.tileMap.rect.z = -0.01
        # imageRect = EasyPygame.Rect(16 / 512, 64 / 512, 16 / 512, 16 / 512)
        # self.tileMap.addTextureView(TileTextureView("animated.png", imageRect))
        # self.tileMap.useTextureView(1)

        # character = GameObject(self, "Character")
        # for i in range(4):
        #     imageRect = EasyPygame.Rect(128 / 512 + 16 / 512 * i, 16 / 512, 16 / 512, 16 / 512)
        #     character.addTextureView(TextureView("animated.png", imageRect.copy(), flipX=True))
        #     character.addTextureView(TextureView("animated.png", imageRect))

        # for i in range(4):
        #     imageRect = EasyPygame.Rect(128 / 512 + 16 / 512 * (i + 4), 16 / 512, 16 / 512, 16 / 512)
        #     character.addTextureView(TextureView("animated.png", imageRect.copy(), flipX=True))
        #     character.addTextureView(TextureView("animated.png", imageRect))

        # # 1: leftIdle, 2: rightIdle, 3:leftRun, 4:rightRun
        # character.FSM.addState(idle("a", "d", 3, 4))
        # character.FSM.addState(idle("d", "a", 4, 3))
        # character.FSM.addState(run("a", "d", 1, 4))
        # character.FSM.addState(run("d", "a", 2, 3))

        # # 1357LeftIdle, 2468RightIdle, 9111315LeftRun, 10121416RightRun
        # character.FSM.attachConcurrentState(1, SpriteAnimState(500, [1, 3, 5, 7]))
        # character.FSM.attachConcurrentState(2, SpriteAnimState(500, [2, 4, 6, 8]))
        # character.FSM.attachConcurrentState(3, SpriteAnimState(250, [9, 11, 13, 15]))
        # character.FSM.attachConcurrentState(4, SpriteAnimState(250, [10, 12, 14, 16]))

        # character.FSM.switchState(1, 0)
        # self.characters.append(character)

        # self.floor = Floor(self, 33, 33)
        # self.floor.randomize([(0,0)])

        # self.skinChanger = SkinChanger()
        # self.robot2 = Robot(self)
        # self.robot2.changeSkin(self.skinChanger)
        # self.robot = Robot(self)
        # self.robot.changeSkin(self.skinChanger)

        # self.mmap = Map((20, 20), [], [(5, 3)], (0, 0))
        # self.behavior = BehaviorGoFast()
        # self.pathFinder = VisitOrderProducer(BFS(DSFactory()))
        # self.behavior.go(self.robot, self.mmap, self.pathFinder)

        self.testObj = GameObject(self, "test")
        self.testObj.worldRects = []
        self.testObj.addTextureView(DefaultInstancedTextureView(self.testObj.worldRects))
        self.testObj.useTextureView(1)

        for i in range(100):
            rect = EasyPygame.Rect(i * 1.1, 0, 1, 1)
            self.testObj.worldRects.append(rect)

    def preRender(self, ms):
        EasyPygame.pprint("This is Scene1", 0, 0)

    def postRender(self, ms):
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

        if EasyPygame.isDown1stTime("m"):
            self.robot.move()
        if EasyPygame.isDown1stTime("r"):
            self.robot.rotate()

    def onUnLoad(self):
        EasyPygame.unload("animated.png")


if __name__ == "__main__":
    EasyPygame.initWindow(800, 800, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()
