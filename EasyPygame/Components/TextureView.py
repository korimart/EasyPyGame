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

        try:
            if self.fitObject:
                EasyPygame.drawStretchedImage(self.texture, rect, self.imageRect)
            else:
                EasyPygame.drawImage(self.texture, rect, self.imageRect)
        except:
            DefaultTextureView.srender(gameObject, camera)

class DefaultTextureView:
    @staticmethod
    def srender(gameObject, camera):
        rect = gameObject.rect.copy()
        x, y = camera.view([rect.x, rect.y])
        rect.x = x
        rect.y = y
        EasyPygame.drawRect((0, 0, 255), rect)
        EasyPygame.pprint(gameObject.name, x, y, True)

    def render(self, gameObject, camera):
        DefaultTextureView.srender(gameObject, camera)
