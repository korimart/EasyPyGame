import EasyPygame

class TextureView:
    def __init__(self, texture, imageRect=None, minFilter="nearest", \
            magFilter="nearest", flipX=False, flipY=False):

        self.texture = texture
        if not imageRect:
            self.imageRect = EasyPygame.Rect(0, 0, 1, 1)
        else:
            self.imageRect = imageRect
        self.flipX = flipX
        self.flipY = flipY
        self.minFilter = minFilter
        self.magFilter = magFilter

    def render(self, gameObject):
        EasyPygame.renderer.renderTextured(gameObject.rect.copy(), self)

class TileTextureView(TextureView):
    def __init__(self, texture, imageRect=None, minFilter="nearest", \
            magFilter="nearest", flipX=False, flipY=False, pivot=(0, 0)):
        super().__init__(texture, imageRect, minFilter, magFilter, flipX, flipY)
        self.pivot = pivot

    def render(self, gameObject):
        camPos = gameObject.scene.camera.pos
        rt = gameObject.rect
        x = round((camPos[0] - self.pivot[0]) / rt.width) * rt.width + self.pivot[0]
        y = round((camPos[1] - self.pivot[1]) / rt.height) * rt.height + self.pivot[1]
        dd = 2 * gameObject.scene.camera.distance
        n = max(dd / rt.width, dd / rt.height) + 3
        EasyPygame.renderer.renderTexInstancedCluster((x, y, rt.z), gameObject.rect.width, gameObject.rect.height, self, int(n))

class InstancedTextureView(TextureView):
    def __init__(self, texture, rectListRef, imageRect=None, minFilter="nearest", \
            magFilter="nearest", flipX=False, flipY=False):
        super().__init__(texture, imageRect, minFilter, magFilter, flipX, flipY)
        self.rectListRef = rectListRef

    def render(self, gameObject):
        EasyPygame.renderer.renderTexInstancedIndivi(self.rectListRef, self)

class DefaultTextureView:
    def __init__(self, color=(0, 0, 1.0)):
        self.color = color

    def render(self, gameObject):
        EasyPygame.renderer.renderDefault(gameObject.rect.copy(), self.color, gameObject.name)

class InvisibleTextureView:
    def render(self, gameObject):
        pass