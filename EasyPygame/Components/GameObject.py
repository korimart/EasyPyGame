import EasyPygame
from EasyPygame.Components import TextureView
from EasyPygame.Components import InputHandler

class GameObject:
    def __init__(self, scene, name="GameObject"):
        self.rect = EasyPygame.Rect(0, 0, 100, 100)
        self.textureView = TextureView.DefaultTextureView()
        self.inputHandler = InputHandler.InputHandler()
        self.scene = scene
        self.name = name
        self.z = 0
        scene.addGameObject(self)

    def update(self, ms):
        self.inputHandler.update(self, ms)

    def render(self, ms):
        self.textureView.render(self, self.scene.camera)

    def __eq__(self, other):
        return self.z == other.z

    def __lt__(self, other):
        return self.z < other.z