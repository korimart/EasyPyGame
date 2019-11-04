import EasyPygame
from EasyPygame.Components import Renderer
from EasyPygame.Components import InputHandler

class GameObject:
    def __init__(self, scene, name="GameObject"):
        scene.gameObjects.append(self)
        self.rect = EasyPygame.Rect(0, 0, 100, 100)
        self.renderer = Renderer.DefaultRenderer()
        self.inputHandler = InputHandler.InputHandler()
        self.scene = scene
        self.name = name

    def update(self, ms):
        self.inputHandler.update(self, ms)

    def render(self, ms):
        self.renderer.update(self, self.scene.camera)