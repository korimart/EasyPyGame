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
        EasyPygame.renderer.renderTextured(gameObject.rect.copy(), camera, self)

class DefaultTextureView:
    def __init__(self, color=(0, 0, 255)):
        self.color = color

    def render(self, gameObject, camera):
        EasyPygame.renderer.renderDefault(gameObject.rect.copy(), camera, self.color, gameObject.name)

class InvisibleTextureView:
    def render(self, gameObject, camera):
        pass