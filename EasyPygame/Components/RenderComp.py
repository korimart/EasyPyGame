from random import randint
import EasyPygame

class DefaultRenderComponent:
    def __init__(self, color=(0, 0, 1), showName=True):
        self.color = color
        self.handle = str(randint(0, 100000000))
        self.madeTexture = False

    def render(self, gameObject):
        if not self.madeTexture:
            EasyPygame.resManager.createTextTexture(self.handle, "monogram.ttf", 30, gameObject.name, (0, 0, 0))
            self.madeTexture = True
        EasyPygame.renderer.renderColor(gameObject.transform, self.color)