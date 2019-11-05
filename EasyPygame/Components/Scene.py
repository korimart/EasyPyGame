import EasyPygame.Components.Camera
import EasyPygame

class DefaultScene:
    def __init__(self):
        self.gameObjects = []
        self.camera = EasyPygame.Components.Camera.Camera()

    def load(self):
        pass

    def unload(self):
        pass

    def update(self, ms):
        for gobj in reversed(self.gameObjects):
            gobj.update(ms)

    def preRender(self):
        pass

    def render(self, ms):
        for gobj in reversed(self.gameObjects):
            gobj.render(ms)

    def postRender(self):
        pass

    def addGameObject(self, obj):
        self.gameObjects.append(obj)
        self.gameObjects.sort()

class Scene(DefaultScene):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        EasyPygame.sceneManager.registerScene(cls)
