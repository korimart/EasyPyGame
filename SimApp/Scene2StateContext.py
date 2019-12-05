import EasyPygame
from EasyPygame.Components import *
from SimApp.SIM import SIMProgramSide

class ReadyState(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.buttonList[0].enable(1)

    def onExit(self, gameObject, ms):
        gameObject.buttonList[0].disable()
        gameObject.SIM.go()

class SimulatingState(GameObjectState):
    def update(self, gameObject, ms):
        gameObject.SIM.update(ms, gameObject.cwal)

class NoResponseState(GameObjectState):
    def __init__(self):
        self.responsed = False

    def onEnter(self, gameObject, ms):
        gameObject.cwalText.enable()
        gameObject.cwalText2.enable()

    def update(self, gameObject, ms):
        self.responsed = True
        gameObject.SIM.update(ms, self.cwal)
        if self.responsed:
            gameObject.switchState(gameObject.simulating, ms)
        elif EasyPygame.isDown1stTime("r"):
            gameObject.reset()
            gameObject.SIM.terminateAddOn()
        elif EasyPygame.isDown1stTime("RETURN"):
            gameObject.restart()
            gameObject.SIM.terminateAddOn()

    def onExit(self, gameObject, ms):
        gameObject.cwalText.disable()
        gameObject.cwalText2.disable()

    def cwal(self):
        self.responsed = False

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
        self.speed = 1

        self.SIM = SIMProgramSide(scene, self)

        # start, restart, reset
        self.buttonList = []
        self._makeButtons()

        self.ready      = self.addState(ReadyState())
        self.simulating = self.addState(SimulatingState())
        self.done       = self.addState(DoneState())
        self.noResponse = self.addState(NoResponseState())

        self.speedText = GUI.Text(scene, font="monogram.ttf", color=(1, 1, 1))
        self.speedText.setText("Speed: " + str(self.speed) + "UBD")
        self.speedText.transform.translate(-3, 2.7, 0)
        self.speedText.transform.scale(0.5, 0.5)
        self.cwalText = GUI.Text(scene, text="Cannot wait any longer!", font="monogram.ttf", color=(1, 0, 0))
        self.cwalText2 = GUI.Text(scene, text="Press Enter to restart or R to reset", font="monogram.ttf", color=(1, 0, 0))
        self.cwalText.transform.translate(-3, 2.2, 0)
        self.cwalText.transform.scale(0.3, 0.3)
        self.cwalText.disable()
        self.cwalText2.transform.translate(-3, 1.9, 0)
        self.cwalText2.transform.scale(0.3, 0.3)
        self.cwalText2.disable()

        self.switchState(self.ready, 0)

    def _makeButtons(self):
        self.buttonList.append(GUI.Button(self.scene, name="Start",   callback=lambda: self.start()))
        self.buttonList.append(GUI.Button(self.scene, name="Restart", callback=lambda: self.restart()))
        self.buttonList.append(GUI.Button(self.scene, name="Reset",   callback=lambda: self.reset()))

        for button in self.buttonList:
            button.transform.translate(2, -2, 0)
            button.disable()

        self.buttonList[-1].transform.translate(-1.5, 0, 0)

    def cwal(self):
        self.switchState(self.noResponse, 0)

    def start(self):
        self.switchState(self.simulating, 0)

    def finished(self):
        self.switchState(self.done, 0)

    def restart(self):
        self.scene.restart()

    def reset(self):
        EasyPygame.nextScene("Scene2", "Scene1")

    def yourLogic(self, ms):
        dirty = False
        if EasyPygame.isDown1stTime(","):
            if self.speed > 1:
                self.speed -= 1
                self.SIM.scaleSpeed(1 / 2)
                dirty = True
        if EasyPygame.isDown1stTime("."):
            self.SIM.scaleSpeed(2)
            self.speed += 1
            dirty = True
        if EasyPygame.isDown1stTime("b"):
            self.SIM.floor.blackSheepWall()

        if dirty:
            self.speedText.setText("Speed: " + str(self.speed) + "UBD")
