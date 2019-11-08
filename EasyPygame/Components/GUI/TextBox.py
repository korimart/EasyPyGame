import EasyPygame
from EasyPygame.Components import GameObject
from EasyPygame.Components import InputHandler
from EasyPygame.Components import DefaultTextureView
from EasyPygame.Components import GameObjectState

class TextBoxInputHandlerUnfocused(InputHandler):
    pass

class TextBoxStateFocused(GameObjectState):
    pass

class TextBox(GameObject):
    def __init__(self, scene, name="TextBox"):
        super().__init__(scene, name)
        self.text = ""

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text