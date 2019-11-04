import EasyPygame

class Renderer:
    def __init__(self, texture):
        self.texture = texture

    def update(self, gameObject):
        EasyPygame.drawImage(self.texture, gameObject.rect)

class DefaultRenderer:
    def update(self, gameObject):
        EasyPygame.drawRect((0, 0, 255), gameObject.rect)