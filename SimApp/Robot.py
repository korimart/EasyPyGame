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

ROBOTZ = 0.02

class Working(GameObjectState):
    def __init__(self):
        self.elapsed = 0

    def onEnter(self, gameObject, ms):
        self.elapsed = 0
        gameObject.isWorking = True
        gameObject.renderComp = gameObject.idleRC

    def update(self, gameObject, ms):
        self.elapsed += ms
        if self.elapsed * gameObject.workSpeed > 1:
            gameObject.switchState(gameObject.idle, ms)

class Rotating(GameObjectState):
    def __init__(self):
        self.elapsed = 0
        self.destAngle = 0

    def onEnter(self, gameObject, ms):
        self.elapsed = 0
        self.destAngle = -gameObject.facing % 4 * 90
        gameObject.isWorking = True
        gameObject.renderComp = gameObject.idleRC

    def update(self, gameObject, ms):
        gameObject.arrow.transform.rotate(gameObject.workSpeed * ms * -90)
        self.elapsed += ms
        if self.elapsed * gameObject.workSpeed > 1:
            gameObject.switchState(gameObject.idle, ms)
            gameObject.transform.reset()
            gameObject.transform.rotate(self.destAngle)
            gameObject.transform.translate(0, 1, 0)

class Idle(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.isWorking = False
        gameObject.renderComp = gameObject.idleRC

class Running(GameObjectState):
    def __init__(self):
        self.destX = None
        self.destY = None
        self.deltaX = None
        self.deltaY = None
        self.elapsed = 0

    def onEnter(self, gameObject, ms):
        gameObject.renderComp = gameObject.runningRC
        gameObject.isWorking = True
        self.deltaX = MOVEDELTA[gameObject.facing][0] * gameObject.num
        self.deltaY = MOVEDELTA[gameObject.facing][1] * gameObject.num
        self.destX = gameObject.x + self.deltaX
        self.destY = gameObject.y + self.deltaY
        self.elapsed = 0

    def update(self, gameObject, ms):
        self.elapsed += ms
        deltaX = self.deltaX * gameObject.runSpeed * ms
        deltaY = self.deltaY * gameObject.runSpeed * ms
        gameObject.transform.translate(deltaX, deltaY, 0)

        if gameObject.runSpeed * self.elapsed > 1:
            gameObject.switchState(gameObject.idle, ms)

    def onExit(self, gameObject, ms):
        gameObject.transform.setTranslate(self.destX, self.destY, ROBOTZ)
        gameObject.x, gameObject.y = self.destX, self.destY

class Robot(GameObject):
    def __init__(self, scene):
        super().__init__(scene, "Robot")
        self.transform.translate(0, 0, ROBOTZ)
        self.x = 0
        self.y = 0
        self.facing = Direction.UP
        self.lastFace = Direction.RIGHT
        self.workSpeed = 0.01 # work per ms
        self.runSpeed = 0.01 # block per ms
        self.isWorking = False
        self.num = None

        self.idle = self.addState(Idle())
        self.rotating = self.addState(Rotating())
        self.working = self.addState(Working())
        self.running = self.addState(Running())

        self.idleRC = None
        self.workingRC = None
        self.runningRC = None

        self.arrow = GameObject(scene, "RobotArrow")
        self.arrow.transform.setParent(self.transform)
        self.arrow.transform.translate(0, 1, 0)

    def move(self, num=1):
        if self.facing in [Direction.RIGHT, Direction.LEFT]:
            self.lastFace = self.facing
            self._flipX()
        self.num = num
        self.switchState(self.running, 0)

    def getPos(self):
        self.switchState(self.working, 0)
        return (self.rect.x, self.rect.y, self.facing)

    def rotate(self):
        self.facing = (self.facing + 1) % 4
        self.switchState(self.rotating, 0)

    def changeSkin(self, skinChanger):
        skinChanger.changeRobot(self)

    def nextPos(self, num=2):
        return (self.rect.x + MOVEDELTA[self.facing][0] * num, \
            self.rect.y + MOVEDELTA[self.facing][1] * num)

    # def yourLogic(self, ms):
    #     if EasyPygame.isDown1stTime(","):
    #         self.workTime += 100
    #         if self.runSpeed - 0.001 > 0:
    #             self.runSpeed -= 0.001
    #     elif EasyPygame.isDown1stTime("."):
    #         if self.workTime - 100 > 0:
    #             self.workTime -= 100
    #         self.runSpeed += 0.001

    def _flipX(self):
        self.idleRC.flipX = not self.idleRC.flipX
        self.workingRC.flipX = not self.workingRC.flipX
        self.runningRC.flipX = not self.runningRC.flipX