class FSM:
    def __init__(self, gameObject):
        self.gameObjectStateDict = dict()
        self.currentState = GameObjectState()
        self.gameObject = gameObject

    def addState(self, state):
        if state.__class__.__name__ not in self.gameObjectStateDict:
            self.gameObjectStateDict[state.__class__.__name__] = state

    def switchState(self, stateName, ms):
        try:
            self.currentState = self.gameObjectStateDict[stateName]
            self.currentState.onEnter(self.gameObject, ms)
        except:
            raise Exception("GameObjectState not registered in FSM")
    
    def update(self, ms):
        self.currentState.update(self.gameObject, ms)

class GameObjectState:
    def onEnter(self, gameObject, ms):
        pass

    def update(self, gameObject, ms):
        pass

    def onExit(self, gameObject, ms):
        pass