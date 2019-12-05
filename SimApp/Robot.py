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

ROBOTZ = 0.015

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
        self.startAngle = self.destAngle + 90
        gameObject.isWorking = True
        gameObject.renderComp = gameObject.idleRC

    def update(self, gameObject, ms):
        self.elapsed += ms
        gameObject.arrow.transform.reset()
        gameObject.arrow.transform.rotate(gameObject.rotationSpeed * self.elapsed * -90)
        gameObject.arrow.transform.rotate(self.startAngle)
        gameObject.arrow.transform.translate(0, 1, 0)

        if self.elapsed * gameObject.rotationSpeed > 1:
            gameObject.arrow.transform.reset()
            gameObject.arrow.transform.rotate(self.destAngle)
            gameObject.arrow.transform.translate(0, 1, 0)
            gameObject.switchState(gameObject.idle, ms)

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
        gameObject.scene.camera.move((deltaX, deltaY))

        if gameObject.runSpeed * self.elapsed > 1:
            gameObject.switchState(gameObject.idle, ms)

    def onExit(self, gameObject, ms):
        gameObject.transform.setTranslate(self.destX, self.destY, ROBOTZ)
        gameObject.x, gameObject.y = self.destX, self.destY
        gameObject.scene.camera.moveTo(self.destX, self.destY)

class Robot(GameObject):
    def __init__(self, scene):
        super().__init__(scene, "Robot")
        self.transform.translate(0, 0, ROBOTZ)
        self.x = 0
        self.y = 0
        self.facing = Direction.UP
        self.lastFace = Direction.RIGHT
        self.workSpeed = 0.001 # work per ms
        self.runSpeed = 0.001 # block per ms
        self.rotationSpeed = 0.001
        self.isWorking = False
        self.num = None
        self.workBuffer = []

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
        self.workBuffer.append((self._move, (num,)))

    def _move(self, num):
        if self.facing in [Direction.RIGHT, Direction.LEFT]:
            if self.facing is not self.lastFace:
                self.lastFace = self.facing
                self._flipX()
        self.num = num
        self.switchState(self.running, 0)

    def getPos(self):
        self.workBuffer.append((self._getPos, tuple()))

    def _getPos(self):
        self.switchState(self.working, 0)
        return (self.x, self.y, self.facing)

    def rotate(self):
        self.workBuffer.append((self._rotate, tuple()))

    def _rotate(self):
        self.facing = (self.facing + 1) % 4
        self.switchState(self.rotating, 0)

    def work(self):
        if not self.isWorking and self.workBuffer:
            pop = self.workBuffer.pop()
            pop[0](*pop[1])

    def hasWork(self):
        return bool(self.workBuffer)

    def changeSkin(self, skinChanger):
        skinChanger.changeRobot(self)

    def nextPos(self, num=2):
        return (self.x + MOVEDELTA[self.facing][0] * num, \
            self.y + MOVEDELTA[self.facing][1] * num)

    def scaleWorkSpeed(self, scale):
        self.workSpeed *= scale

    def scaleMoveSpeed(self, scale):
        self.runSpeed *= scale

    def scaleRotationSpeed(self, scale):
        self.rotationSpeed *= scale

    def _flipX(self):
        self.idleRC.renderComp.flipX = not self.idleRC.renderComp.flipX
        self.runningRC.renderComp.flipX = not self.runningRC.renderComp.flipX