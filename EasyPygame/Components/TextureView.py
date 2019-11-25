import EasyPygame

class TextureView:
    def __init__(self, texture, imageRect=None, stretchFit=True, \
            cropFit=False, halign="center", \
            flipX=False, flipY=False):

        self.texture = texture
        if not imageRect:
            self.imageRect = EasyPygame.Rect(0, 0, 1, 1)
        else:
            self.imageRect = imageRect
        self.stretchFit = stretchFit
        self.cropFit = cropFit
        self.halign = halign
        self.flipX = flipX
        self.flipY = flipY

    def render(self, gameObject):
        gameObject.screenRect = EasyPygame.renderer.renderTextured( \
            gameObject.rect.copy(), self)

class TileTextureView(TextureView):
    def __init__(self, texture, imageRect=None, stretchFit=True, \
            cropFit=False, halign="center", \
            flipX=False, flipY=False, n=1):
            super().__init__(texture, imageRect, stretchFit, cropFit, halign, flipX, flipY)
            self.n = n

    def render(self, gameObject):
        cam = gameObject.scene.camera
        EasyPygame.renderer.renderTexInstancedPos(cam.pos, gameObject.rect.width, gameObject.rect.height, self, self.n)

    def setN(self, n):
        if n > 0:
            self.n = n

class DefaultTextureView:
    def __init__(self, color=(0, 0, 1.0)):
        self.color = color

    def render(self, gameObject):
        gameObject.screenRect = EasyPygame.renderer.renderDefault( \
            gameObject.rect.copy(), self.color, gameObject.name)

class InvisibleTextureView:
    def render(self, gameObject):
        gameObject.screenRect = None