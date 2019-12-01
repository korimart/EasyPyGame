import multiprocessing
import queue
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

class SIMProgramSide:
    def __init__(self, scene, parent, patience=5000):
        self.parent = parent
        self.sendingQueue = None
        self.receivingQueue = None
        self.patience = patience
        self.patienceMeter = 0
        self.ret = None
        self.needReturn = False

        self.robot = Robot(scene)
        self.floor = Floor(scene, parent.width, parent.height)
        self.skinChanger = DungeonSkinChanger()
        self.robot.changeSkin(self.skinChanger)

        self.floor.randomize(parent.startPos, parent.targetPosList, parent.knownHazardsList)

        # test--- uncover all
        hazards = self.floor.getHazardList()
        for hazard in hazards:
            self.floor.uncover(*hazard)
        # test--- uncover all

        self.addOn = AddOn()
        self.addOn.setMap((parent.width, parent.height), [], parent.startPos, parent.targetPosList)

    def update(self, ms, cwal):
        if self.floor.colorTileBuffer:
            return

        self.patienceMeter += ms
        self._handleMessage()
        if self.robot.isWorking:
            return

        if self.needReturn:
            self.robotReturn(self.ret)
            self.needReturn = False

        if self.patienceMeter > self.patience:
            cwal()

    def go(self):
        self.progPipe, self.addOnPipe = multiprocessing.Pipe(True)
        process = multiprocessing.Process(target=self._go, args=(self.addOn, self.addOnPipe))
        process.start()

    @staticmethod
    def _go(addOn, pipe):
        sim = SIMAddOnSide(pipe)
        addOn.go(sim)

    def _handleMessage(self):
        if not self.progPipe.poll():
            return

        message = self.progPipe.recv()

        if message == Message.MOVE:
            self.ret = self.robot.move()
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

        else:
            raise Exception("Unknown message from addOn")

        self.needReturn = True
        self.patienceMeter = 0

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

    def _returnRobotMessage(self, message):
        self.pipe.send(message)
        return self.pipe.recv()