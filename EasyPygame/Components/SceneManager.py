from EasyPygame import Components

class SceneManager:
    def __init__(self):
        self.sceneClassDict = dict()
        self.sceneInstanceDict = dict()
        self.currentScene = Components.DefaultScene()

    def registerScene(self, sceneCls):
        if sceneCls.__name__ in self.sceneClassDict:
            return
        
        self.sceneClassDict[sceneCls.__name__] = sceneCls

    def loadScene(self, sceneName):
        if sceneName in self.sceneInstanceDict:
            return

        try:
            scene = self.sceneClassDict[sceneName]()
            scene.load()
            self.sceneInstanceDict[sceneName] = scene
        except:
            raise Exception("Scene not defined")

    def unloadScene(self, sceneName):
        if self.currentScene.__class__.__name__ == sceneName:
            raise Exception("Trying to unload current scene")

        try:
            scene = self.sceneInstanceDict[sceneName]
            scene.unload()
            del self.sceneInstanceDict[sceneName]
        except:
            return

    def getScene(self, sceneName):
        try:
            return self.sceneInstanceDict[sceneName]
        except:
            return None

    def switchScene(self, sceneName):
        try:
            self.currentScene = self.sceneInstanceDict[sceneName]
        except:
            raise Exception("Scene specified not loaded")