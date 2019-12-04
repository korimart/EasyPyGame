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
        self.speed = 0

        self.SIM = SIMProgramSide(scene, self)

        # start, restart, reset
        self.buttonList = []
        self._makeButtons()

        self.ready      = self.addState(ReadyState())
        self.simulating = self.addState(SimulatingState())
        self.done       = self.addState(DoneState())

        self.text = GUI.Text(scene, font="monogram.ttf", color=(1, 1, 1))
        self.text.transform.translate(-3, 2.7, 0)
        self.text.transform.scale(0.5, 0.5)
        self.text.setText("Speed: " + str(self.speed) + " UBD")

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
        #print("cannot wait any longer")
        pass

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
            if self.speed > 0:
                self.speed -= 1
                self.SIM.scaleSpeed(1 / 1.2)
                dirty = True
        if EasyPygame.isDown1stTime("."):
            self.SIM.scaleSpeed(1.2)
            self.speed += 1
            dirty = True
        if EasyPygame.isDown1stTime("b"):
            self.SIM.floor.blackSheepWall()

        if dirty:        
            self.text.setText("Speed: " + str(self.speed) + " UBD")
