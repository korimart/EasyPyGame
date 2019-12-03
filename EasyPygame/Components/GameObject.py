import EasyPygame
import EasyPygame.Components as Cmp

class GameObject:
    def __init__(self, scene, name="GameObject"):
        scene.addGameObject(self)
        self.scene = scene
        self.transform = Cmp.TransformComp()
        self.renderComp = Cmp.InvisibleRenderComponent()
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
        self.renderComp.render(self)

    def disable(self):
        self.switchState(0, 0)

    def enable(self, stateIndex):
        self.switchState(stateIndex, 0)

    def isMouseOn(self):
        camera = self.scene.camera
        mousePos = EasyPygame.getMousePos()
        x, y = camera.screen2worldCoord(mousePos, self.rect.z)
        try:
            return self.rect.collidepoint(x, y)
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

    def __eq__(self, other):
        return self.rect.z == other.rect.z

    def __lt__(self, other):
        return self.rect.z < other.rect.z

class GameObjectState:
    def onEnter(self, gameObject, ms):
        pass

    def update(self, gameObject, ms):
        pass

    def onExit(self, gameObject, ms):
        pass

class StaticTextureState(GameObjectState):
    def __init__(self, staticTextureViewIndex):
        self.staticTextureViewIndex = staticTextureViewIndex

    def onEnter(self, gameObject, ms):
        if self.staticTextureViewIndex >= 0:
            gameObject.useTextureView(self.staticTextureViewIndex)

class SpriteAnimState(GameObjectState):
    def __init__(self, duration, textureViewIndexList):
        self.duration = duration
        self.textureViewIndexList = textureViewIndexList
        self.ms = 0

        try:
            self.msPerFrame = duration / len(textureViewIndexList)
        except ZeroDivisionError:
            self.msPerFrame = duration
            self.textureViewIndexList = [0]

    def update(self, gameObject, ms):
        index = int(self.ms / self.msPerFrame)
        gameObject.useTextureView(self.textureViewIndexList[index])
        self.ms += ms
        self.ms %= self.duration

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