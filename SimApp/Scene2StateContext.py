import EasyPygame

class Scene2StateContext(EasyPygame.Components.GameObject):
    def __init__(self, scene, width, height, startPos, targetPosList, knownHazardsList):
        super().__init__(scene, "SceneState")
        self.scene = scene
        self.width = width
        self.height = height
        self.startPos = startPos
        self.targetPosList = targetPosList
        self.knownHazardsList = knownHazardsList

        # start, restart, reset
        self.buttonList = []
        self._makeButtons()

    def _makeButtons(self):
        self.buttonList.append(EasyPygame.Components.GUI.Button(self.scene, "startButton", lambda: self.start()))
        self.buttonList.append(EasyPygame.Components.GUI.Button(self.scene, "restartButton", lambda: self.restart()))
        self.buttonList.append(EasyPygame.Components.GUI.Button(self.scene, "resetButton", lambda: self.reset()))

        for button in self.buttonList:
            button.disable()

    def start(self):
        pass

    def finished(self):
        pass

    def restart(self):
        pass

    def reset(self):
        pass

    def setState(self, stateIndex, ms):
        self.FSM.switchState(stateIndex, ms)