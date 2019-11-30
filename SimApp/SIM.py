import multiprocessing
import queue
from SimApp.Floor import Floor
from SimApp.Robot import Robot
from AddOn.AddOn import AddOn

class Message:
    MOVE = 0
    ROTATE = 1
    GETPOS = 2
    SENSEBLOB = 3
    SENSEHAZARD = 4

class SIMProgramSide:
    def __init__(self, scene, patience=3000):
        self.robot = Robot(scene)
        self.floor = Floor(scene, 20, 20)
        self.sendingQueue = None
        self.receivingQueue = None
        self.patience = patience
        self.patienceMeter = 0

        # test
        self.hazards = []
        self.floor.randomize([(19, 19)])
        terrain = self.floor.terrain
        for i in range(20):
            for j in range(20):
                if terrain[i][j]:
                    self.hazards.append((j, i))

    def update(self, ms, cwal):
        self.robot.update(ms)
        if self.robot.isWorking:
            return

        self.patienceMeter += ms
        self._handleMessage()

        if self.patienceMeter > self.patience:
            cwal()

    def go(self):
        self.sendingQueue = multiprocessing.Queue(maxsize=1)
        self.receivingQueue = multiprocessing.Queue(maxsize=1)
        process = multiprocessing.Process(target=self._go, args=(self.hazards, self.receivingQueue, self.sendingQueue))
        process.start()

    @staticmethod
    def _go(hazards, sendingQueueForAddOn, receivingQueueForAddOn):
        sim = SIMAddOnSide(sendingQueueForAddOn, receivingQueueForAddOn)
        addOn = AddOn(hazards)
        addOn.go(sim)

    def _handleMessage(self):
        try:
            message = self.receivingQueue.get(block=False)
        except queue.Empty:
            return

        if message == Message.MOVE:
            self.robot.move()
        elif message == Message.ROTATE:
            self.robot.rotate()
        elif message == Message.GETPOS:
            self.robot.getPos()
        elif message == Message.SENSEBLOB:
            # ask floor
            pass
        elif message == Message.SENSEHAZARD:
            # ask floor
            pass
        else:
            raise Exception("Unknown message from addOn")

        self.patienceMeter = 0

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