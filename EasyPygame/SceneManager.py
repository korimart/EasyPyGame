from EasyPygame import Components

class SceneManager:
    def __init__(self):
        self.sceneClassDict = dict()
        self.sceneInstanceDict = dict()
        self.currentScene = Components.DefaultScene()
        self.loadSceneNameList = []
        self.unloadSceneNameList = []
        self.switchSceneName = ""
        self.loadSceneCallOnLoad = []

    def registerScene(self, sceneCls):
        if sceneCls.__name__ in self.sceneClassDict:
            return
        
        self.sceneClassDict[sceneCls.__name__] = sceneCls

    def loadScene(self, sceneName):
        self.loadSceneNameList.append(sceneName)

    def _loadScene(self):
        for sceneName in self.loadSceneNameList:
            if sceneName in self.sceneInstanceDict:
                continue

            try:
                scene = self.sceneClassDict[sceneName]()
            except:
                raise Exception("Scene not defined")
            scene.onLoad()
            self.sceneInstanceDict[sceneName] = scene
        
        for callInfo in self.loadSceneCallOnLoad:
            try:
                scene = self.getScene(callInfo[0])
                func = getattr(scene, callInfo[1])
                func(*callInfo[2])
            except:
                raise Exception("Wrong func or arg in nextSceneOnLoad")
        
        self.loadSceneNameList = []
        self.loadSceneCallOnLoad = []

    def unloadScene(self, sceneName):
        self.unloadSceneNameList.append(sceneName)

    def _unloadScene(self):
        for sceneName in self.unloadSceneNameList:
            try:
                scene = self.sceneInstanceDict[sceneName]
                scene.onUnload()
                del self.sceneInstanceDict[sceneName]
            except:
                continue
        
        self.unloadSceneNameList = []

    def getScene(self, sceneName):
        try:
            return self.sceneInstanceDict[sceneName]
        except:
            return None

    def switchScene(self, sceneName):
        self.switchSceneName = sceneName

    def loadSceneOnLoad(self, sceneName, funcName, argTuple):
        self.loadSceneCallOnLoad.append((sceneName, funcName, argTuple))

    def update(self):
        self._loadScene()
        self._unloadScene()
        self._switchScene()

    def _switchScene(self):
        if self.switchSceneName:
            try:
                self.currentScene = self.sceneInstanceDict[self.switchSceneName]
            except:
                raise Exception("Scene specified not loaded")
            finally:
                self.switchSceneName = ""