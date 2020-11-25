from random import randint

import EasyPygame
from EasyPygame.Components import *

class Text(GameObject):
    def __init__(self, scene, name="Text", text="Set Your Text",\
        font="comic.ttf", size=30, color=(0, 0, 0), fixOnCamera=True):

        super().__init__(scene, name)

        if fixOnCamera:
            self.transform.setParent(scene.camera.transform)
            self.transform.translate(0, 0, -scene.camera.DEFAULTDIST)

        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.handle = randint(0, 100000000)
        self.setText(text)
        self.renderComp = TextureRenderComponent(self.handle, blending=True)

    def setText(self, text):
        self.text = text
        width, height = EasyPygame.resManager.createTextTexture(self.handle, self.font, self.size, self.text, self.color)
        ratio = width / height
        self.transform.resetPredefined()
        self.transform.translatePredefined(ratio / 2, 0, 0)
        self.transform.scalePredefined(ratio, 1)
