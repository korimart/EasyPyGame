import EasyPygame
from EasyPygame.Components import GUI

class ReadyState(EasyPygame.Components.GameObjectState):
    def __init__(self):
        super().__init__(0, 0, "Ready")
        self.wasRestart = False

    def onEnter(self, gameObject, ms):
        super().onEnter(gameObject, ms)
        gameObject.buttonList[0].enable(1)
        
        if self.wasRestart:
            # restart SIM and addOn
            # maybe pass addOn to SIM again
            pass

    def onExit(self, gameObject, ms):
        super().onExit(gameObject, ms)
        gameObject.buttonList[0].disable()

class SimulatingState(EasyPygame.Components.GameObjectState):
    def __init__(self):
        super().__init__(0, 0, "Simulating")

    def onEnter(self, gameObject, ms):
        super().onEnter(gameObject, ms)
        # message SIM to start

    def update(self, gameObject, ms):
        super().update(gameObject, ms)
        # update SIM with taking-so-long callback

    def addOnIsTakingSoLong(self):
        # display "waiting calculation"
        pass

class DoneState(EasyPygame.Components.GameObjectState):
    def __init__(self):
        super().__init__(0, 0, "Done")

    def onEnter(self, gameObject, ms):
        super().onEnter(gameObject, ms)
        gameObject.buttonList[1].enable(1)
        gameObject.buttonList[2].enable(1)
        # organize floor and robot for button display

    def onExit(self, gameObject, ms):
        super().onExit(gameObject, ms)
        gameObject.buttonList[1].disable()
        gameObject.buttonList[2].disable()

class Scene2StateContext(EasyPygame.Components.GameObject):
    def __init__(self, scene, width, height, startPos, targetPosList, knownHazardsList):
        super().__init__(scene, "SceneState")
        self.scene = scene
        self.width = width
        self.height = height
        self.startPos = startPos
        self.targetPosList = targetPosList
        self.knownHazardsList = knownHazardsList

        self.SIM = None
        self.addOn = None

        # start, restart, reset
        self.buttonList = []
        self._makeButtons()

        self.ready      = self.FSM.addState(ReadyState())
        self.simulating = self.FSM.addState(SimulatingState())
        self.done       = self.FSM.addState(DoneState())

        self.FSM.switchState(self.ready, 0)

    def _makeButtons(self):
        self.buttonList.append(GUI.Button(self.scene, name="startButton",   callback=lambda: self.start()))
        self.buttonList.append(GUI.Button(self.scene, name="restartButton", callback=lambda: self.restart()))
        self.buttonList.append(GUI.Button(self.scene, name="resetButton",   callback=lambda: self.reset()))

        for button in self.buttonList:
            button.disable()

    def start(self):
        self.FSM.switchState(self.simulating, 0)

    def finished(self):
        self.FSM.switchState(self.done, 0)

    def restart(self):
        self.FSM.getGameStateObject(self.ready).wasRestart = True
        self.FSM.switchState(self.ready)

    def reset(self):
        EasyPygame.nextScene("Scene2", "Scene1")
    