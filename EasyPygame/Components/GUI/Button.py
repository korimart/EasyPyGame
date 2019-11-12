import EasyPygame
from EasyPygame.Components import GameObject
from EasyPygame.Components import InputHandler
from EasyPygame.Components import DefaultTextureView
from EasyPygame.Components import GameObjectState

class ButtonStatePressed(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(gameObject.TVRed)
        gameObject.useInputHandler(3)

class ButtonStateReleased(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(0)
        gameObject.useInputHandler(1)

class ButtonStateHover(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(gameObject.TVGreen)
        gameObject.useInputHandler(2)

class ButtonInputHandlerReleased(InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isMouseOnObject(gameObject):
            gameObject.FSM.switchState(2, ms)

class ButtonInputHandlerPressed(InputHandler):
    def update(self, gameObject, ms):
        if not EasyPygame.isDown(1):
            gameObject.FSM.switchState(1, ms)

class ButtonInputHandlerHover(InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime(1):
            EasyPygame.consume(1)
            gameObject.callback()
            gameObject.FSM.switchState(3, ms)
        elif not EasyPygame.isMouseOnObject(gameObject):
            gameObject.FSM.switchState(1, ms)

class Button(GameObject):
    def __init__(self, scene, buttonName="Button", callback=None):
        super().__init__(scene, buttonName)
        self.callback = callback
        self.addInputHandler(ButtonInputHandlerReleased())
        self.addInputHandler(ButtonInputHandlerHover())
        self.addInputHandler(ButtonInputHandlerPressed())
        self.TVRed = self.addTextureView(DefaultTextureView((255, 0, 0)))
        self.TVGreen = self.addTextureView(DefaultTextureView((0, 255, 0)))
        self.FSM.addState(ButtonStateReleased())
        self.FSM.addState(ButtonStateHover())
        self.FSM.addState(ButtonStatePressed())
        self.FSM.switchState(1, 0)

        self.useInputHandler(1)

    def setCallback(self, callback):
        self.callback = callback