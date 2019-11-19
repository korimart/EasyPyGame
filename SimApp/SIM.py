import multiprocessing

class SIM:
    MAXWAITTIME = 3000
    def __init__(self, addOn):
        self.addOn = addOn
        # init robot and pass SIM for addOn interface
        self.robot = None
        self.process = None
        self.queue = multiprocessing.Queue(maxsize=1)
        self.message = ""
        self.ms = 0
        self.isWaitingForAddOn = False

    def update(self, ms, takingSoLong):
        if self.isWaitingForAddOn:
            self._waitForAddOn(ms, takingSoLong)
        else:
            self._waitForRobot(ms)

    def _waitForRobot(self, ms):
        # if robot.FSM.getState == waiting
        #   self.isWaitingForAddOn = True
        # else
        #   if accelerate:
        #       force robot state switch      
        pass

    def _waitForAddOn(self, ms, takingSoLong):
        try:
            self.message = self.queue.get(block=False)
        except:
            self.message = ""

        if self.message:
            self.ms = 0
            self._handleAddOnMessage()
            self.isWaitingForAddOn = False
        else:
            self.ms += ms
            if self.ms > self.MAXWAITTIME:
                takingSoLong(self.ms)

    def _handleAddOnMessage(self):
        if self.message == "move":
            self.robot.move()
        elif self.message == "rotate":
            self.robot.rotate()
        elif self.message == "getPos":
            self.robot.getPos()
        elif self.message == "senseBlob":
            # ask floor
            pass
        elif self.message == "senseHazard":
            # ask floor
            pass
        else:
            self.message = ""
            raise Exception("Unknown message from addOn")

        self.message = ""

    def move(self):
        self.message = "move"

    def rotate(self):
        self.message = "rotate"

    def getPos(self):
        self.message = "getPos"

    def senseBlob(self):
        self.message = "senseBlob"

    def senseHazard(self):
        self.message = "senseHazard"

    def go(self, robot):
        self.process = multiprocessing.Process(target=self._go, args=tuple(self.addOn, self.queue))
        self.process.start()

    @staticmethod
    def _go(addOn, queue):
        sim = SIM()
        addOn.go(sim)
        queue.put(sim.message)
        