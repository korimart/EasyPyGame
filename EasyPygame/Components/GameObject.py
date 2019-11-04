from abc import abstractmethod
import EasyPygame
from EasyPygame.Components import Renderer

class GameObject:
    def __init__(self, scene):
        scene.gameObjects.append(self)
        self.rect = EasyPygame.Rect(0, 0, 100, 100)
        self.renderer = Renderer.DefaultRenderer()
        self.scene = scene

    def update(self, ms):
        self.handleInput(ms)

    def render(self, ms):
        self.renderer.update(self, self.scene.camera)

    @abstractmethod
    def handleInput(self, ms):
        pass