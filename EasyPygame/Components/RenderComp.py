from random import randint
import EasyPygame

class InvisibleRenderComponent:
    def render(self, gameObject):
        pass

class DefaultRenderComponent:
    def __init__(self, color=(0, 0, 1), showName=True):
        self.color = color
        self.handle = str(randint(0, 100000000))
        self.madeTexture = False

    def render(self, gameObject):
        if not self.madeTexture:
            EasyPygame.resManager.createTextTexture(self.handle, "monogram.ttf", 30, gameObject.name, (0, 0, 0))
            self.madeTexture = True

        renderer = EasyPygame.renderer
        renderer.renderColor(gameObject.transform, self.color)
        renderer.enableBlending()
        textTrans = gameObject.transform.copy()
        textTrans.translate(0, 0, 0.001)
        renderer.renderTexture(textTrans, self.handle)
        renderer.disableBlending()

class DefaultInstancedRenderComponent:
    def __init__(self, transCompList, color=(0, 0, 1), showName=True):
        self.color = color
        self.handle = str(randint(0, 100000000))
        self.madeTexture = False
        self.buffer = EasyPygame.renderer.setInstancingTransComps(transCompList)
        transList = []
        for transform in transCompList:
            t = transform.copy()
            t.translate(0, 0, 0.001)
            transList.append(t)
        self.textBuffer = EasyPygame.renderer.setInstancingTransComps(transList)

    def render(self, gameObject):
        if not self.madeTexture:
            EasyPygame.resManager.createTextTexture(self.handle, "monogram.ttf", 30, gameObject.name, (0, 0, 0))
            self.madeTexture = True

        renderer = EasyPygame.renderer
        renderer.resetSettings()
        renderer.renderColorInstanced(self.buffer, self.color)
        renderer.enableBlending()
        renderer.renderTextureInstanced(self.textBuffer, self.handle)

class TextureRenderComponent:
    def __init__(self, texture, imageRect=None, minFilter="nearest", \
            magFilter="nearest", flipX=False, flipY=False, blending=False):
        self.texture = texture
        self.imageRect = imageRect
        self.flipX = flipX
        self.flipY = flipY
        self.minFilter = minFilter
        self.magFilter = magFilter
        self.blending = blending

    def _settings(self, renderer):
        renderer = EasyPygame.renderer
        if self.blending:
            renderer.enableBlending()
        else:
            renderer.disableBlending()

        renderer.setFlip(self.flipX, self.flipY)
        renderer.setFilter(self.minFilter, self.magFilter)

    def render(self, gameObject):
        renderer = EasyPygame.renderer
        self._settings(renderer)
        renderer.renderTexture(gameObject.transform, self.texture, self.imageRect)

class TextureInstancedRenderComponent(TextureRenderComponent):
    def __init__(self, transCompList, texture, imageRect=None, minFilter='nearest', magFilter='nearest', \
        flipX=False, flipY=False, blending=False):
        super().__init__(texture, imageRect=imageRect, minFilter=minFilter, magFilter=magFilter, \
            flipX=flipX, flipY=flipY, blending=blending)

        self.buffer = EasyPygame.renderer.setInstancingTransComps(transCompList)

    def render(self, gameObject):
        renderer = EasyPygame.renderer
        super()._settings(renderer)
        renderer.renderTextureInstanced(self.buffer, self.texture, self.imageRect)
