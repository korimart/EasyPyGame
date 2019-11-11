import EasyPygame
from EasyPygame.Components import GameObject
from EasyPygame.Components import InputHandler
from EasyPygame.Components import DefaultTextureView
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
                if key not in [1, 2, 3] and EasyPygame.isDown1stTime(key):
                    gameObject.text += chr(key)

class TextBox(GameObject):
    def __init__(self, scene, name="TextBox"):
        super().__init__(scene, name)
        self.text = ""
        self.cursorPos = 0;
        self.addInputHandler(TextBoxInputHandlerUnfocused())
        self.addInputHandler(TextBoxInputHandlerFocused())
        self.useInputHandler(1)

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text