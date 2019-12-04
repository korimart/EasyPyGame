import multiprocessing
import queue
import time
from random import random
from SimApp.Floor import Floor
from SimApp.Robot import *
from AddOn.AddOn import AddOn
from SimApp.SkinChanger import *

class Message:
    MOVE = 0
    ROTATE = 1
    GETPOS = 2
    SENSEBLOB = 3
    SENSEHAZARD = 4
    CLEARCOLOR = 5
    COLORTILE = 6
    # COLORTILEARRAY = 7
    PATH = 7
    CLOSE = 8

class SIMProgramSide:
    def __init__(self, scene, parent, patience=10, errorRate=0.2):
        self.parent = parent
        self.patience = patience
        self.patienceMeter = 0
        self.ret = None
        self.needReturn = False
        self.errorRate = errorRate

        self.robot = Robot(scene)
        self.floor = Floor(scene, parent.width, parent.height)
        self.floor.pathed(*parent.startPos)
        self.skinChanger = DungeonSkinChanger()
        self.robot.changeSkin(self.skinChanger)
        self.close = False

        self.floor.randomize(parent.startPos, parent.targetPosList, parent.knownHazardsList, \
            parent.knownBlobsList)

        self.addOn = AddOn()
        self.addOn.setMap((parent.width, parent.height), [], parent.startPos, parent.targetPosList)

    def update(self, ms, cwal):
        if self.floor.isDrawing():
            return

        count = 0
        thisMS = ms
        self.patienceMeter = 0
        while not self.close:
            start = time.process_time()
            empty = self._handleMessage()

            self.robot.update(0)

            if self.robot.isWorking:
                return

            if self.needReturn:
                self.robotReturn(self.ret)
                self.needReturn = False
                count += 1

            if count > 50:
                break

            thisMS = (time.process_time() - start)
            self.patienceMeter += thisMS * 1000

            if self.patienceMeter > self.patience:
                cwal()
                break

        if self.close:
            self.parent.switchState(self.parent.done, ms)

    def go(self):
        self.progPipe, self.addOnPipe = multiprocessing.Pipe(True)
        process = multiprocessing.Process(target=self._go, args=(self.addOn, self.addOnPipe))
        process.start()

    def scaleSpeed(self, scale):
        self.robot.scaleWorkSpeed(scale)
        self.robot.scaleMoveSpeed(scale)
        self.robot.scaleRotationSpeed(scale)
        self.floor.scalePathDrawSpeed(scale)
        self.floor.scaleTileDrawSpeed(scale)

    @staticmethod
    def _go(addOn, pipe):
        sim = SIMAddOnSide(pipe)
        addOn.go(sim)
        print("end")

    def _handleMessage(self):
        if not self.progPipe.poll():
            return

        message = self.progPipe.recv()

        if message == Message.MOVE:
            num = 1
            self.floor.pathed(*self.robot.nextPos(1))
            if random() < self.errorRate:
                x, y = self.robot.nextPos()
                if not self.floor.senseHazard(x, y):
                    self.floor.pathed(x, y)
                    num = 2
            self.ret = self.robot.move(num)

        elif message == Message.ROTATE:
            self.ret = self.robot.rotate()

        elif message == Message.GETPOS:
            self.ret = self.robot.getPos()

        elif message == Message.SENSEBLOB:
            north = self.floor.senseBlob(self.robot.x, self.robot.y + 1)
            east = self.floor.senseBlob(self.robot.x + 1, self.robot.y)
            south = self.floor.senseBlob(self.robot.x, self.robot.y - 1)
            west = self.floor.senseBlob(self.robot.x - 1, self.robot.y)
            self.ret = [north, east, south, west]

        elif message == Message.SENSEHAZARD:
            self.ret = self.floor.senseHazard(self.robot.x + MOVEDELTA[self.robot.facing][0], self.robot.y + MOVEDELTA[self.robot.facing][1])

        elif message == Message.CLEARCOLOR:
            self.ret = None
            self.floor.clearColor()

        elif message == Message.COLORTILE:
            x, y = self.progPipe.recv()
            self.ret = None
            self.floor.colorTile(x, y)

        elif message == Message.PATH:
            path = self.progPipe.recv()
            self.ret = None
            self.floor.colorPath(path)

        elif message == Message.CLOSE:
            self.close = True
            self.needReturn = False

        else:
            raise Exception("Unknown message from addOn")

        self.needReturn = True
        self.patienceMeter = 0

        return False

    def robotReturn(self, ret):
        self.progPipe.send(ret)

class SIMAddOnSide:
    def __init__(self, pipe):
        self.pipe = pipe

    def move(self):
        return self._returnRobotMessage(Message.MOVE)

    def rotate(self):
        return self._returnRobotMessage(Message.ROTATE)

    def getPos(self):
        return self._returnRobotMessage(Message.GETPOS)

    def senseBlob(self):
        return self._returnRobotMessage(Message.SENSEBLOB)

    def senseHazard(self):
        return self._returnRobotMessage(Message.SENSEHAZARD)

    def clearColor(self):
        return self._returnRobotMessage(Message.CLEARCOLOR)

    def colorTile(self, x, y):
        self.pipe.send(Message.COLORTILE)
        self.pipe.send((int(x), int(y)))
        return self.pipe.recv()

    def colorPath(self, path):
        self.pipe.send(Message.PATH)
        self.pipe.send(path)
        return self.pipe.recv()

    def close(self):
        self.pipe.send(Message.CLOSE)

    def _returnRobotMessage(self, message):
        self.pipe.send(message)
        return self.pipe.recv()