import EasyPygame
from EasyPygame.Components import *

class Direction:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class MoveDelta:
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)

MOVEDELTA = [MoveDelta.UP, MoveDelta.RIGHT, MoveDelta.DOWN, MoveDelta.LEFT]

class Working(GameObjectState):
    def __init__(self):
        self.elapsed = 0

    def onEnter(self, gameObject, ms):
        self.elapsed = 0
        gameObject.isWorking = True

    def update(self, gameObject, ms):
        if self.elapsed < gameObject.workTime:
            self.elapsed += ms
        else:
            gameObject.FSM.switchState(1, ms) # idle

class Idle(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.isWorking = False

class Running(GameObjectState):
    def __init__(self):
        self.destX = None
        self.destY = None
        self.elapsed = 0

    def onEnter(self, gameObject, ms):
        gameObject.isWorking = True
        self.destX = gameObject.rect.x + MOVEDELTA[gameObject.facing][0]
        self.destY = gameObject.rect.y + MOVEDELTA[gameObject.facing][1]
        self.elapsed = 0

    def update(self, gameObject, ms):
        self.elapsed += ms
        deltaX = MOVEDELTA[gameObject.facing][0] * gameObject.runSpeed * ms
        deltaY = MOVEDELTA[gameObject.facing][1] * gameObject.runSpeed * ms
        gameObject.setX(gameObject.rect.x + deltaX)
        gameObject.setY(gameObject.rect.y + deltaY)
        arrow = gameObject.arrow
        arrow.setXYZ(arrow.rect.x + deltaX, arrow.rect.y + deltaY, None)
        gameObject.scene.camera.moveTo(gameObject.rect.x, gameObject.rect.y)

        if gameObject.runSpeed * self.elapsed > 1:
            gameObject.FSM.switchState(gameObject.idle, ms)

    def onExit(self, gameObject, ms):
        gameObject.setXYZ(self.destX, self.destY, None)
        gameObject.arrow.setXYZ(self.destX + MOVEDELTA[gameObject.facing][0], self.destY + MOVEDELTA[gameObject.facing][1], None)
        gameObject.scene.camera.moveTo(gameObject.rect.x, gameObject.rect.y)

class Robot(GameObject):
    def __init__(self, scene):
        super().__init__(scene, "Robot")
        self.rect.z = 0.01
        self.facing = Direction.UP
        self.lastFace = Direction.RIGHT
        self.workTime = 100
        self.runSpeed = 0.01 # 0.001 per ms -> 1 per second
        self.isWorking = False

        self.idle = self.FSM.addState(Idle())
        self.working = self.FSM.addState(Working())
        self.running = self.FSM.addState(Running())

        self.arrow = GameObject(scene, "RobotArrow")
        self.arrow.setXYZ(MOVEDELTA[self.facing][0], MOVEDELTA[self.facing][1], self.rect.z)

    def move(self):
        if self.facing in [Direction.RIGHT, Direction.LEFT]:
            self.lastFace = self.facing
        self.FSM.switchState(self.running, 0)

    def getPos(self):
        self.FSM.switchState(self.working, 0)
        return (self.rect.x, self.rect.y, self.facing)

    def rotate(self):
        self.FSM.switchState(self.working, 0)
        self.facing = (self.facing + 1) % 4
        self.arrow.setXYZ(self.rect.x + MOVEDELTA[self.facing][0], self.rect.y + MOVEDELTA[self.facing][1], None)

    def changeSkin(self, skinChanger):
        skinChanger.changeRobot(self)