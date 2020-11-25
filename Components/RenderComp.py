from random import randint
import EasyPygame
import glm

class InvisibleRenderComponent:
    def render(self, gameObject, ms):
        pass

class DefaultRenderComponent:
    def __init__(self, color=(0, 0, 1), showName=True):
        self.color = color
        self.handle = str(randint(0, 100000000))
        self.madeTexture = False
        self.showName = showName

    def render(self, gameObject, ms):
        if not self.madeTexture:
            EasyPygame.resManager.createTextTexture(self.handle, "monogram.ttf", 30, gameObject.name, (0, 0, 0))
            self.madeTexture = True

        renderer = EasyPygame.renderer
        renderer.resetSettings()
        renderer.renderColor(gameObject.transform.getWorldMat(), self.color)
        renderer.enableBlending()
        if self.showName:
            textTrans = gameObject.transform.copy()
            textTrans.translate(0, 0, 0.001)
            renderer.renderTexture(textTrans.getWorldMat(), self.handle)
            renderer.disableBlending()

class DefaultInstancedRenderComponent:
    def __init__(self, worldList, color=(0, 0, 1), showName=True, size=None, static=True):
        self.color = color
        self.handle = str(randint(0, 100000000))
        self.madeTexture = False
        self.num = len(worldList) if worldList else 0
        self.buffer = EasyPygame.renderer.setInstancingWorlds(worldList, size, static)
        self.showName = showName

        if not worldList:
            worldList = []

        self.worlds = []
        self.textWorlds = []
        for world in worldList:
            t = glm.mat4(world)
            self.worlds.append(t)
            t = glm.translate(world, glm.vec3(0, 0, 0.001))
            self.textWorlds.append(t)

        self.buffer = EasyPygame.renderer.setInstancingWorlds(self.worlds, size, static)
        self.textBuffer = EasyPygame.renderer.setInstancingWorlds(self.textWorlds, size, static)

    def render(self, gameObject, ms):
        if not self.madeTexture:
            EasyPygame.resManager.createTextTexture(self.handle, "monogram.ttf", 30, gameObject.name, (0, 0, 0))
            self.madeTexture = True

        if self.num:
            renderer = EasyPygame.renderer
            renderer.resetSettings()
            renderer.renderColorInstanced(self.buffer, self.color, self.num)
            if self.showName:
                renderer.enableBlending()
                renderer.renderTextureInstanced(self.textBuffer, self.num, self.handle)

    def clear(self):
        self.worlds = []
        self.textWorlds = []
        self.num = 0

    def append(self, world):
        self.worlds.append(glm.mat4(world))
        self.textWorlds.append(glm.mat4(world))
        EasyPygame.renderer.updateInstancingWorlds(self.buffer, self.num, [world])
        self.num += 1

    def __del__(self):
        EasyPygame.renderer.deleteBuffer(self.buffer)
        EasyPygame.renderer.deleteBuffer(self.textBuffer)

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

    def render(self, gameObject, ms):
        renderer = EasyPygame.renderer
        self._settings(renderer)
        renderer.renderTexture(gameObject.transform.getWorldMat(), self.texture, self.imageRect)

class TextureInstancedRenderComponent(TextureRenderComponent):
    def __init__(self, worldList, texture, size=None, imageRect=None, minFilter='nearest', magFilter='nearest', \
        flipX=False, flipY=False, blending=False, static=True):
        super().__init__(texture, imageRect=imageRect, minFilter=minFilter, magFilter=magFilter, \
            flipX=flipX, flipY=flipY, blending=blending)

        self.num = len(worldList) if worldList else 0
        self.buffer = EasyPygame.renderer.setInstancingWorlds(worldList, size, static)
        if not worldList:
            worldList = []
        self.worlds = [glm.mat4(world) for world in worldList]

    def render(self, gameObject, ms):
        if self.num:
            renderer = EasyPygame.renderer
            super()._settings(renderer)
            renderer.renderTextureInstanced(self.buffer, self.num, self.texture, self.imageRect)

    def clear(self):
        self.worlds = []
        self.num = 0

    def append(self, world):
        self.worlds.append(glm.mat4(world))
        EasyPygame.renderer.updateInstancingWorlds(self.buffer, self.num, [world])
        self.num += 1

    def __del__(self):
        EasyPygame.renderer.deleteBuffer(self.buffer)

# class AnimationRenderComponent:
#     def __init__(self, renderCompList, duration):
#         self.compList = renderCompList
#         self.duration = duration
#         self.ms = 0

#         try:
#             self.msPerFrame = duration / len(renderCompList)
#         except ZeroDivisionError:
#             self.msPerFrame = duration
#             self.compList = [DefaultRenderComponent()]

#     def render(self, gameObject, ms):
#         index = int(self.ms / self.msPerFrame)
#         self.compList[index].render(gameObject, ms)
#         self.ms += ms
#         self.ms %= self.duration

class AnimationRenderComponent:
    def __init__(self, renderComponent, imageRectList, duration):
        self.renderComp = renderComponent
        self.rectList = imageRectList
        self.duration = duration
        self.ms = 0

        try:
            self.msPerFrame = duration / len(imageRectList)
        except ZeroDivisionError:
            self.msPerFrame = duration
            self.compList = [None]

    def render(self, gameObject, ms):
        index = int(self.ms / self.msPerFrame)
        self.renderComp.imageRect = self.rectList[index]
        self.renderComp.render(gameObject, ms)
        self.ms += ms
        self.ms %= self.duration

    def append(self, world):
        try:
            self.renderComp.append(world)
        except:
            pass

    def clear(self):
        try:
            self.renderComp.clear()
        except:
            pass