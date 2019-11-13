import EasyPygame
from EasyPygame.Components import GameObject
from EasyPygame.Components import InputHandler
from EasyPygame.Components import DefaultTextureView, TextureView
from EasyPygame.Components import GameObjectState

class TextBoxInputHandlerUnfocused(InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime(1) and EasyPygame.isMouseOnObject(gameObject):
            gameObject.useInputHandler(2)

class TextBoxInputHandlerFocused(InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime(1) and not EasyPygame.isMouseOnObject(gameObject):
            gameObject.useInputHandler(1)
        else:
            keyList = EasyPygame.inputManager.thisInputList.copy()
            for key in keyList:
                if 32 <= key <= 126 and EasyPygame.isDown1stTime(chr(key)): # ascii printables
                    gameObject.text += chr(key)
                    gameObject.curosrPos += 1

class TextBox(GameObject):
    def __init__(self, scene, name="TextBox"):
        super().__init__(scene, name)
        self.text = ""
        self.cursorPos = 0;
        self.addInputHandler(TextBoxInputHandlerUnfocused())
        self.addInputHandler(TextBoxInputHandlerFocused())
        self.useInputHandler(1)
        self.charTextureView = TextureView("__KorimartChar")
        self.addTextureView(self.charTextureView)
        self.useTextureView(1)
        self._prepareTexture("TTTT")

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text

    def yourLogic(self, ms):
        pass

    def _prepareTexture(self, char):
        EasyPygame.createTextImage(EasyPygame.DEFAULT_FONT, EasyPygame.DEFAULT_FONT_SIZE, (0, 0, 0), "__KorimartChar", char, True)
        