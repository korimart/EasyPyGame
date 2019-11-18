class FSM:
    def __init__(self, gameObject):
        self.currentStateIndex = 0
        self.gameObjectStateList = [GameObjectState()]
        self.animationStateDict = dict()
        self.gameObject = gameObject

    def addState(self, state):
        self.gameObjectStateList.append(state)
        return len(self.gameObjectStateList) - 1

    def attachAnimationState(self, gameObjectStateIndex, animationState):
        try:
            self.animationStateDict[gameObjectStateIndex].append(animationState)
        except KeyError:
            self.animationStateDict[gameObjectStateIndex] = [animationState]

    def switchState(self, stateIndex, ms):
        if 0 <= stateIndex < len(self.gameObjectStateList):
            if self.currentStateIndex in self.animationStateDict:
                for animationState in self.animationStateDict[self.currentStateIndex]:
                    animationState.onExit(self.gameObject, ms)
            self.gameObjectStateList[self.currentStateIndex].onExit(self.gameObject, ms)

            self.currentStateIndex = stateIndex
        else:
            self.currentStateIndex = 0

        self.gameObjectStateList[self.currentStateIndex].onEnter(self.gameObject, ms)
        if self.currentStateIndex in self.animationStateDict:
            for animationState in self.animationStateDict[self.currentStateIndex]:
                animationState.onEnter(self.gameObject, ms)

    def getGameStateObject(self, index):
        return self.gameObjectStateList[index]

    def update(self, ms):
        self.gameObjectStateList[self.currentStateIndex].update(self.gameObject, ms)
        if self.currentStateIndex in self.animationStateDict:
            for animationState in self.animationStateDict[self.currentStateIndex]:
                animationState.update(self.gameObject, ms)

class GameObjectState:
    def __init__(self, inputHandlerIndex=0, staticTextureViewIndex=0):
        self.inputHandlerIndex = inputHandlerIndex
        self.staticTextureViewIndex = staticTextureViewIndex

    def onEnter(self, gameObject, ms):
        gameObject.useInputHandler(self.inputHandlerIndex)
        if self.staticTextureViewIndex >= 0:
            gameObject.useTextureView(self.staticTextureViewIndex)

    def update(self, gameObject, ms):
        pass

    def onExit(self, gameObject, ms):
        pass

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

    def onEnter(self, gameObject, ms):
        self.ms = 0

    def update(self, gameObject, ms):
        index = int(self.ms / self.msPerFrame)
        gameObject.useTextureView(self.textureViewIndexList[index])
        self.ms += ms
        self.ms %= self.duration