import random

import EasyPygame
from EasyPygame.Components import GameObject
from EasyPygame.Components import DefaultTextureView, TextureView
from EasyPygame.Components import GameObjectState, SpriteAnimState

class TextBoxUnfocused(GameObjectState):
    def onEnter(self, gameObject, ms):
        super().onEnter(gameObject, ms)
        EasyPygame.createTextImage(gameObject.fontName, gameObject.fontSize, \
            gameObject.color, gameObject.textureName, gameObject.text, True, \
            (200, 200, 200))

    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("MOUSELEFT") and gameObject.isMouseOn():
            gameObject.FSM.switchState(2, ms)

class TextBoxFocused(GameObjectState):
    def update(self, gameObject, ms):
        EasyPygame.createTextImage(gameObject.fontName, gameObject.fontSize, \
            gameObject.color, gameObject.textureName, gameObject.text, True, \
            (50, 50, 210))
        surf = EasyPygame.resManager.getLoaded(gameObject.textureName)
        gameObject.charTextureView.halign = "right" \
            if surf.get_width() > gameObject.rect.width else "left"

        if EasyPygame.isDown1stTime("RETURN") \
            or EasyPygame.isDown1stTime("MOUSELEFT") and not gameObject.isMouseOn():
            gameObject.FSM.switchState(1, ms)
        elif EasyPygame.isDown1stTime("BACKSPACE"):
            gameObject.text = gameObject.text[:-1]
            gameObject.cursorPos -= 1
        else:
            printables = EasyPygame.inputManager.getPrintables()
            gameObject.text += "".join(printables)
            gameObject.cursorPos += len(printables)

class TextBox(GameObject):
    def __init__(self, scene, name="TextBox", defaultText="", \
            fontName="comicsansms", fontSize=30, color=(0,0,0)):
        super().__init__(scene, name)
        self.text = defaultText
        self.cursorPos = 0;
        self.fontName = fontName
        self.fontSize = fontSize
        self.color = color
        self.textureName = "__Kori" + str(random.randint(0, 10000))

        self.charTextureView = TextureView(self.textureName, \
            stretchFit=False, halign="left", cropFit=True)
        self.addTextureView(self.charTextureView)

        self.FSM.addState(TextBoxUnfocused(1))
        self.FSM.addState(TextBoxFocused(1))
        self.FSM.switchState(1, 0)

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text