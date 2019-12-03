import random

import EasyPygame
from EasyPygame.Components import *

class TextBoxUnfocused(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.modifyTextureView()
        gameObject.bg.renderComp.color = (0.8, 0.8, 0.8)

    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("MOUSELEFT") and gameObject.isMouseOn():
            gameObject.switchState(2, ms)

class TextBoxFocused(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.bg.renderComp.color = (0.2, 0.2, 0.9)

    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("RETURN") \
            or EasyPygame.isDown1stTime("MOUSELEFT") and not gameObject.isMouseOn():
            gameObject.switchState(1, ms)
        elif EasyPygame.isDown1stTime("BACKSPACE"):
            gameObject.text = gameObject.text[:-1]
            gameObject.dirty = True
        else:
            printables = EasyPygame.inputManager.getPrintables()
            if printables:
                gameObject.text += "".join(printables)
                gameObject.dirty = True

        if gameObject.dirty:
            gameObject.modifyTextureView()
            gameObject.dirty = False

class TextBox(GameObject):
    def __init__(self, scene, width, name="TextBox", defaultText="", \
            fontName="monogram.ttf", color=(0,0,0)):
        super().__init__(scene, name)
        self.text = defaultText
        self.fontName = fontName
        self.color = color
        self.dirty = False
        self.ratio = width

        while True:
            self.textureName = "__Kori" + str(random.randint(0, 10000))
            try:
                EasyPygame.resManager.getTexture(self.textureName)
            except:
                break

        self.renderComp = TextureRenderComponent(self.textureName, blending=True)

        self.bg = GameObject(scene, name + "BG")
        self.bg.transform.setParent(self.transform)
        self.bg.transform.translate(0, 0, -0.01)
        self.bg.renderComp = DefaultRenderComponent((0.8, 0.8, 0.8), showName=False)

        self.addState(TextBoxUnfocused())
        self.addState(TextBoxFocused())
        self.switchState(1, 0)

    def modifyTextureView(self):
        if self.text:
            width, height = EasyPygame.resManager.createTextTexture(self.textureName, self.fontName, \
                72, self.text, self.color)
            ratio = width / height
            imageWidth = self.ratio / ratio
            imageRect = EasyPygame.Rect(0, 0, imageWidth, 1)
            if imageWidth < 1:
                imageRect.x = 1 - imageWidth
            self.renderComp.imageRect = imageRect
        else:
            self.renderComp.imageRect.width = 0

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text