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
    COLORTILEARRAY = 7
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

        self.floor.randomize(parent.startPos, parent.targetPosList, parent.knownHazardsList)


        self.addOn = AddOn()
        self.addOn.setMap((parent.width, parent.height), [], parent.startPos, parent.targetPosList)

    def update(self, ms, cwal):
        if self.floor.colorTileBuffer:
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
            self.parent.FSM.switchState(self.parent.done, ms)

    def go(self):
        self.progPipe, self.addOnPipe = multiprocessing.Pipe(True)
        process = multiprocessing.Process(target=self._go, args=(self.addOn, self.addOnPipe))
        process.start()

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
            north = self.floor.senseBlob(self.robot.rect.x, self.robot.rect.y + 1)
            east = self.floor.senseBlob(self.robot.rect.x + 1, self.robot.rect.y)
            south = self.floor.senseBlob(self.robot.rect.x, self.robot.rect.y - 1)
            west = self.floor.senseBlob(self.robot.rect.x - 1, self.robot.rect.y)
            self.ret = [north, east, south, west]

        elif message == Message.SENSEHAZARD:
            self.ret = self.floor.senseHazard(self.robot.rect.x + MOVEDELTA[self.robot.facing][0], self.robot.rect.y + MOVEDELTA[self.robot.facing][1])

        elif message == Message.CLEARCOLOR:
            self.ret = None
            self.floor.clearColor()

        elif message == Message.COLORTILE:
            x = self.progPipe.recv()
            y = self.progPipe.recv()
            self.ret = None
            self.floor.colorTile(x, y)

        elif message == Message.COLORTILEARRAY:
            tupleList = self.progPipe.recv()
            for pos in tupleList:
                self.floor.colorTile(*pos)

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
        self.pipe.send(int(x))
        self.pipe.send(int(y))
        return self.pipe.recv()

    def colorTileArray(self, tupleList):
        self.pipe.send(Message.COLORTILEARRAY)
        self.pipe.send(tupleList)
        return self.pipe.recv()

    def close(self):
        self.pipe.send(Message.CLOSE)

    def _returnRobotMessage(self, message):
        self.pipe.send(message)
        return self.pipe.recv()