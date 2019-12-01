import EasyPygame.Components.Camera
import EasyPygame

class DefaultScene:
    def __init__(self):
        self.gameObjects = []
        self.camera = EasyPygame.Components.Camera.Camera()

    def onLoad(self):
        pass

    def onUnload(self):
        pass

    def update(self, ms):
        for gobj in reversed(self.gameObjects):
            gobj.update(ms)
        for gobj in reversed(self.gameObjects):
            gobj.yourLogic(ms)

    def preRender(self, ms):
        pass

    def render(self, ms):
        for gobj in reversed(self.gameObjects):
            gobj.render(ms)

    def postRender(self, ms):
        pass

    def addGameObject(self, obj):
        self.gameObjects.append(obj)
        self.gameObjects.sort()

class Scene(DefaultScene):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        EasyPygame.sceneManager.registerScene(cls)
