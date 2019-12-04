import EasyPygame
from EasyPygame.Components import *
from SimApp.SIM import SIMProgramSide

class ReadyState(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.buttonList[0].enable(1)

    def onExit(self, gameObject, ms):
        gameObject.buttonList[0].disable()

class SimulatingState(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.SIM.go()

    def update(self, gameObject, ms):
        gameObject.SIM.update(ms, gameObject.cwal)

class DoneState(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.buttonList[1].enable(1)
        gameObject.buttonList[2].enable(1)

    def onExit(self, gameObject, ms):
        gameObject.buttonList[1].disable()
        gameObject.buttonList[2].disable()

class Scene2StateContext(GameObject):
    def __init__(self, scene, width, height, startPos, targetPosList, knownHazardsList, knownBlobsList):
        super().__init__(scene, "SceneState")
        self.scene = scene
        self.width = width
        self.height = height
        self.startPos = startPos
        self.targetPosList = targetPosList
        self.knownHazardsList = knownHazardsList
        self.knownBlobsList = knownBlobsList

        self.SIM = SIMProgramSide(scene, self)

        # start, restart, reset
        self.buttonList = []
        self._makeButtons()

        self.ready      = self.addState(ReadyState())
        self.simulating = self.addState(SimulatingState())
        self.done       = self.addState(DoneState())

        self.switchState(self.ready, 0)

    def _makeButtons(self):
        self.buttonList.append(GUI.Button(self.scene, name="Start",   callback=lambda: self.start()))
        self.buttonList.append(GUI.Button(self.scene, name="Restart", callback=lambda: self.restart()))
        self.buttonList.append(GUI.Button(self.scene, name="Reset",   callback=lambda: self.reset()))

        for button in self.buttonList:
            button.transform.translate(2, -2, 0)
            button.disable()

        self.buttonList[-1].transform.setTranslate(0.5, 0, 0)

    def cwal(self):
        pass
        #print("cannot wait any longer")

    def start(self):
        self.switchState(self.simulating, 0)

    def finished(self):
        self.switchState(self.done, 0)

    def restart(self):
        self.scene.restart()

    def reset(self):
        EasyPygame.nextScene("Scene2", "Scene1")
