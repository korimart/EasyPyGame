import EasyPygame

class TextureView:
    def __init__(self, texture, imageRect=None, fitObject=True, crop=False, halign="center", relPos=(0, 0), scale=(1.0, 1.0)):
        self.texture = texture
        self.imageRect = imageRect
        self.fitObject = fitObject
        self.crop = crop
        self.relPos = relPos
        self.halign = halign
        self.scale = scale

    def render(self, gameObject, camera):
        EasyPygame.renderer.render(gameObject.rect.copy(), camera, self)

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

class InvisibleTextureView:
    def render(self, gameObject, camera):
        pass