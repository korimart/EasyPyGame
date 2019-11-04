import EasyPygame

class Renderer:
    def __init__(self, texture):
        self.texture = texture

    def update(self, gameObject, camera):
        rect = gameObject.rect.copy()
        x, y = camera.view([rect.x, rect.y])
        rect.x = x
        rect.y = y
        EasyPygame.drawImage(self.texture, rect)

class DefaultRenderer:
    def update(self, gameObject, camera):
        rect = gameObject.rect.copy()
        x, y = camera.view([rect.x, rect.y])
        rect.x = x
        rect.y = y
        EasyPygame.drawRect((0, 0, 255), rect)