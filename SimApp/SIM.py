import multiprocessing
import queue
from SimApp.Floor import Floor
from SimApp.Robot import *
from AddOn.AddOn import AddOn
from SimApp.SkinChanger import SkinChanger

class Message:
    MOVE = 0
    ROTATE = 1
    GETPOS = 2
    SENSEBLOB = 3
    SENSEHAZARD = 4

class SIMProgramSide:
    def __init__(self, scene, parent, patience=3000):
        self.parent = parent
        self.sendingQueue = None
        self.receivingQueue = None
        self.patience = patience
        self.patienceMeter = 0
        self.ret = None
        self.needReturn = False

        self.robot = Robot(scene)
        self.floor = Floor(scene, parent.width, parent.height)
        self.addOn = AddOn()
        self.skinChanger = SkinChanger()
        self.robot.changeSkin(self.skinChanger)

        self.floor.randomize(parent.startPos, parent.targetPosList)

        # test--- uncover all
        hazards = self.floor.getHazardList()
        for hazard in hazards:
            self.floor.uncover(*hazard)
        # test--- uncover all

        self.addOn.setMap((parent.width, parent.height), [], parent.startPos, parent.targetPosList)

    def update(self, ms, cwal):
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
        self.sendingQueue = multiprocessing.Queue(maxsize=1)
        self.receivingQueue = multiprocessing.Queue(maxsize=1)
        process = multiprocessing.Process(target=self._go, args=(self.addOn, self.receivingQueue, self.sendingQueue))
        process.start()

    @staticmethod
    def _go(addOn, sendingQueueForAddOn, receivingQueueForAddOn):
        sim = SIMAddOnSide(sendingQueueForAddOn, receivingQueueForAddOn)
        addOn.go(sim)

    def _handleMessage(self):
        try:
            message = self.receivingQueue.get(block=False)
        except queue.Empty:
            return

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
        else:
            raise Exception("Unknown message from addOn")

        self.patienceMeter = 0
        self.needReturn = True

    def robotReturn(self, ret):
        self.sendingQueue.put(ret)

class SIMAddOnSide:
    def __init__(self, sendingQueue, receivingQueue):
        self.sendingQueue = sendingQueue
        self.receivingQueue = receivingQueue

    def move(self):
        self.sendingQueue.put(Message.MOVE)
        return self._returnRobotMessage()

    def rotate(self):
        self.sendingQueue.put(Message.ROTATE)
        return self._returnRobotMessage()

    def getPos(self):
        self.sendingQueue.put(Message.GETPOS)
        return self._returnRobotMessage()

    def senseBlob(self):
        self.sendingQueue.put(Message.SENSEBLOB)
        return self._returnRobotMessage()

    def senseHazard(self):
        self.sendingQueue.put(Message.SENSEHAZARD)
        return self._returnRobotMessage()

    def _returnRobotMessage(self):
        return self.receivingQueue.get()