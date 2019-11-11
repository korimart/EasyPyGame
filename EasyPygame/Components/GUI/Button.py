import EasyPygame
from EasyPygame.Components import GameObject
from EasyPygame.Components import InputHandler
from EasyPygame.Components import DefaultTextureView
from EasyPygame.Components import GameObjectState

class ButtonStatePressed(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(gameObject.TVRed)
        gameObject.useInputHandler(gameObject.IHPressed)

class ButtonStateReleased(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(0)
        gameObject.useInputHandler(gameObject.IHReleased)

class ButtonStateHover(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(gameObject.TVGreen)
        gameObject.useInputHandler(gameObject.IHHover)

class ButtonInputHandlerReleased(InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isMouseOnObject(gameObject):
            gameObject.FSM.switchState("ButtonStateHover", ms)

class ButtonInputHandlerPressed(InputHandler):
    def update(self, gameObject, ms):
        if not EasyPygame.isDown(1):
            gameObject.FSM.switchState("ButtonStateReleased", ms)

class ButtonInputHandlerHover(InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime(1):
            EasyPygame.consume(1)
            gameObject.callback()
            gameObject.FSM.switchState("ButtonStatePressed", ms)
        elif not EasyPygame.isMouseOnObject(gameObject):
            gameObject.FSM.switchState("ButtonStateReleased", ms)

class Button(GameObject):
    def __init__(self, scene, buttonName="Button", callback=None):
        super().__init__(scene, buttonName)
        self.callback = callback
        self.IHReleased = self.addInputHandler(ButtonInputHandlerReleased())
        self.IHPressed = self.addInputHandler(ButtonInputHandlerPressed())
        self.IHHover = self.addInputHandler(ButtonInputHandlerHover())
        self.TVRed = self.addTextureView(DefaultTextureView((255, 0, 0)))
        self.TVGreen = self.addTextureView(DefaultTextureView((0, 255, 0)))
        self.FSM.addState(ButtonStatePressed())
        self.FSM.addState(ButtonStateReleased())
        self.FSM.addState(ButtonStateHover())

        self.useInputHandler(self.IHReleased)

    def setCallback(self, callback):
        self.callback = callback