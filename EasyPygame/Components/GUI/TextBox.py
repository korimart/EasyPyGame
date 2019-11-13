import EasyPygame
from EasyPygame.Components import GameObject
from EasyPygame.Components import InputHandler
from EasyPygame.Components import DefaultTextureView, TextureView
from EasyPygame.Components import GameObjectState, SpriteAnimState

class TextBoxInputHandlerUnfocused(InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("MOUSELEFT") and EasyPygame.isMouseOnObject(gameObject):
            gameObject.useInputHandler(2)

class TextBoxInputHandlerFocused(InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("RETURN") or EasyPygame.isDown1stTime("MOUSELEFT") and not EasyPygame.isMouseOnObject(gameObject):
            gameObject.useInputHandler(1)
        elif EasyPygame.isDown1stTime("BACKSPACE"):
            gameObject.text = gameObject.text[:-1]
            gameObject.cursorPos -= 1
        else:
            printables = EasyPygame.inputManager.getPrintables()
            gameObject.text += "".join(printables)
            gameObject.cursorPos += len(printables)

class TextBox(GameObject):
    def __init__(self, scene, name="TextBox", fontName="comicsansms", fontSize=30, color=(0,0,0)):
        super().__init__(scene, name)
        self.text = "abc"
        self.cursorPos = 0;
        self.fontName = fontName
        self.fontSize = fontSize
        self.color = color

        self.addInputHandler(TextBoxInputHandlerUnfocused())
        self.addInputHandler(TextBoxInputHandlerFocused())
        self.useInputHandler(1)
        self.charTextureView = TextureView("__KorimartChar", None, False, True, "left")
        self.addTextureView(self.charTextureView)
        self.useTextureView(1)

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text

    def yourLogic(self, ms):
        EasyPygame.createTextImage(self.fontName, self.fontSize, self.color, "__KorimartChar", self.text, True)
        surf = EasyPygame._getImageSurf("__KorimartChar")
        self.charTextureView.align = "right" if surf.get_width() > self.rect.width else "left"
