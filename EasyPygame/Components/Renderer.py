import EasyPygame

class Renderer:
    def __init__(self, texture, imageRect=None, fitObject=True):
        self.texture = texture
        self.imageRect = imageRect
        self.fitObject = fitObject

    def update(self, gameObject, camera):
        rect = gameObject.rect.copy()
        x, y = camera.view([rect.x, rect.y])
        rect.x = x
        rect.y = y

        if self.fitObject:
            EasyPygame.drawStretchedImage(self.texture, rect, self.imageRect)
        else:
            EasyPygame.drawImage(self.texture, rect, self.imageRect)

class DefaultRenderer:
    def update(self, gameObject, camera):
        rect = gameObject.rect.copy()
        x, y = camera.view([rect.x, rect.y])
        rect.x = x
        rect.y = y
        EasyPygame.drawRect((0, 0, 255), rect)
        EasyPygame.pprint(gameObject.name, x, y, True)
