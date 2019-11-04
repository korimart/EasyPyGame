from abc import abstractmethod
import EasyPygame
from EasyPygame.Components import Renderer

class GameObject:
    def __init__(self):
        self.renderer = Renderer.Renderer(None, 1)
        self.rect = EasyPygame.Rect(0, 0, 0, 0)

    def update(self, ms):
        self.handleInput(ms)

    def render(self, ms):
        self.renderer.update(self)

    @abstractmethod
    def handleInput(self, ms):
        pass