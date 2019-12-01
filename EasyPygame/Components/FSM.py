class FSM:
    def __init__(self, gameObject):
        self.currentStateIndex = 0
        self.gameObjectStateList = [GameObjectState()]
        self.concurrentStateDict = dict()
        self.gameObject = gameObject

    def addState(self, state):
        self.gameObjectStateList.append(state)
        return len(self.gameObjectStateList) - 1

    def attachConcurrentState(self, gameObjectStateIndex, state):
        try:
            self.concurrentStateDict[gameObjectStateIndex].append(state)
        except KeyError:
            self.concurrentStateDict[gameObjectStateIndex] = [state]

    def clearConcurrentStates(self):
        self.concurrentStateDict = dict()

    def switchState(self, stateIndex, ms):
        if 0 <= stateIndex < len(self.gameObjectStateList):
            if self.currentStateIndex in self.concurrentStateDict:
                for conState in self.concurrentStateDict[self.currentStateIndex]:
                    conState.onExit(self.gameObject, ms)
            self.gameObjectStateList[self.currentStateIndex].onExit(self.gameObject, ms)

            self.currentStateIndex = stateIndex
        else:
            self.currentStateIndex = 0

        self.gameObjectStateList[self.currentStateIndex].onEnter(self.gameObject, ms)
        if self.currentStateIndex in self.concurrentStateDict:
            for conState in self.concurrentStateDict[self.currentStateIndex]:
                conState.onEnter(self.gameObject, ms)

    def getGameObjectState(self, index):
        return self.gameObjectStateList[index]

    def getCurrentState(self):
        return self.gameObjectStateList[self.currentStateIndex]

    def update(self, ms):
        self.gameObjectStateList[self.currentStateIndex].update(self.gameObject, ms)
        if self.currentStateIndex in self.concurrentStateDict:
            for conState in self.concurrentStateDict[self.currentStateIndex]:
                conState.update(self.gameObject, ms)

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
