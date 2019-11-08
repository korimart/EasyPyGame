import EasyPygame

class TextureView:
    def __init__(self, texture, imageRect=None, fitObject=True):
        self.texture = texture
        self.imageRect = imageRect
        self.fitObject = fitObject

    def render(self, gameObject, camera):
        rect = gameObject.rect.copy()
        x, y = camera.view([rect.x, rect.y])
        rect.x = x
        rect.y = y

        if self.fitObject:
            EasyPygame.drawStretchedImage(self.texture, rect, self.imageRect)
        else:
            EasyPygame.drawImage(self.texture, rect, self.imageRect)

class DefaultTextureView:
    def __init__(self, color=(0, 0, 255)):
        self.color = color

    def render(self, gameObject, camera):
        rect = gameObject.rect.copy()
        x, y = camera.view([rect.x, rect.y])
        rect.x = x
        rect.y = y
        EasyPygame.drawRect(self.color, rect)
        EasyPygame.pprint(gameObject.name, x, y, True)
