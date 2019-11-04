import EasyPygame

class Renderer:
    def __init__(self, texture, scale):
        self.texture = texture
        self.scale = scale

    def update(self, gameObject):
        rect = gameObject.screenRect.copy()
        rect.x *= self.scale
        EasyPygame.drawImage(self.texture, rect)