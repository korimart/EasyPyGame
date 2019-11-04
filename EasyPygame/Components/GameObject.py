from abc import abstractmethod
import EasyPygame
from EasyPygame.Components import Renderer

class GameObject:
    def __init__(self):
        self.rect = EasyPygame.Rect(0, 0, 100, 100)
        self.renderer = Renderer.DefaultRenderer()

    def update(self, ms):
        self.handleInput(ms)

    def render(self, ms):
        self.renderer.update(self)

    @abstractmethod
    def handleInput(self, ms):
        pass