import EasyPygame
import EasyPygame.Components as Cmp

class GameObject:
    def __init__(self, scene, name="GameObject"):
        scene.addGameObject(self)
        self.scene = scene
        self.transform = Cmp.TransformComp()
        self.renderComp = Cmp.InvisibleRenderComponent()
        self._renderCompTemp = None
        self.name = name
        self.currentStateIndex = 0
        self.stateList = [GameObjectState()]
        self.concurrentStateDict = dict()

    def update(self, ms):
        self.stateList[self.currentStateIndex].update(self, ms)
        if self.currentStateIndex in self.concurrentStateDict:
            for conState in self.concurrentStateDict[self.currentStateIndex]:
                conState.update(self, ms)

    def yourLogic(self, ms):
        pass

    def render(self, ms):
        self.renderComp.render(self, ms)

    def disable(self):
        self._renderCompTemp = self.renderComp
        self.renderComp = EasyPygame.Components.InvisibleRenderComponent()
        self.switchState(0, 0)

    def enable(self, stateIndex):
        self.renderComp = self._renderCompTemp
        self.switchState(stateIndex, 0)

    def isMouseOn(self):
        camera = self.scene.camera
        mousePos = EasyPygame.getMousePos()
        x, y = camera.screen2worldCoord(mousePos, self.transform.getZ())
        try:
            return self.transform.collidepoint(x, y)
        except AttributeError:
            return False

    def addState(self, state):
        self.stateList.append(state)
        return len(self.stateList) - 1

    def attachConcurrentState(self, gameObjectStateIndex, state):
        try:
            self.concurrentStateDict[gameObjectStateIndex].append(state)
        except KeyError:
            self.concurrentStateDict[gameObjectStateIndex] = [state]

    def clearConcurrentStates(self):
        self.concurrentStateDict = dict()

    def switchState(self, stateIndex, ms):
        if 0 <= stateIndex < len(self.stateList):
            if self.currentStateIndex in self.concurrentStateDict:
                for conState in self.concurrentStateDict[self.currentStateIndex]:
                    conState.onExit(self.gameObject, ms)
            self.stateList[self.currentStateIndex].onExit(self, ms)

            self.currentStateIndex = stateIndex
        else:
            self.currentStateIndex = 0

        self.stateList[self.currentStateIndex].onEnter(self, ms)
        if self.currentStateIndex in self.concurrentStateDict:
            for conState in self.concurrentStateDict[self.currentStateIndex]:
                conState.onEnter(self, ms)

    def getGameObjectState(self, index):
        return self.stateList[index]

    def getCurrentState(self):
        return self.stateList[self.currentStateIndex]

class GameObjectState:
    def onEnter(self, gameObject, ms):
        pass

    def update(self, gameObject, ms):
        pass

    def onExit(self, gameObject, ms):
        pass

class TerneryState(GameObjectState):
    def __init__(self, condVar, unaryFunc, state1, state2):
        self.condVar = condVar
        self.unaryFunc = unaryFunc
        self.state1 = state1
        self.state2 = state2
        self.currState = None

    def setCondVar(self, condVar):
        self.condVar = condVar

    def setUnaryFunc(self, unaryFunc):
        self.unaryFunc = unaryFunc

    def onEnter(self, gameObject, ms):
        left = getattr(gameObject, self.condVar)
        boolean = self.unaryFunc(left)
        self.currState = self.state1 if boolean else self.state2
        self.currState.onEnter(gameObject, ms)

    def update(self, gameObject, ms):
        self.currState.update(gameObject, ms)

    def onExit(self, gameObject, ms):
        self.currState.onExit(gameObject, ms)