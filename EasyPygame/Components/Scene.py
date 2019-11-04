import EasyPygame.Components.Camera

class Scene:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gameObjects = []
        self.camera = EasyPygame.Components.Camera.Camera(self)

    def update(self, ms):
        for gobj in self.gameObjects:
            gobj.update(ms)

    def render(self, ms):
        for gobj in self.gameObjects:
            gobj.render(ms)