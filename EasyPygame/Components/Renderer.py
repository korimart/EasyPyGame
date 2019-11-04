import EasyPygame

class Renderer:
    def __init__(self, texture, scale):
        self.texture = texture
        self.scale = scale

    def update(self, gameObject):
        if self.texture:
            rect = gameObject.rect.copy()
            rect.x *= self.scale
            EasyPygame.drawImage(self.texture, rect)