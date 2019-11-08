import EasyPygame
from EasyPygame.Components import GameObject
from EasyPygame.Components import InputHandler
from EasyPygame.Components import DefaultTextureView
from EasyPygame.Components import GameObjectState

class ButtonStatePressed(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(1)

class ButtonStateReleased(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(0)

class ButtonInputHandler(InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime(1):
            if EasyPygame.isMouseOnObject(gameObject):
                gameObject.callback()
                gameObject.FSM.switchState("ButtonStatePressed", ms)

        if not EasyPygame.isDown(1) and gameObject.FSM.getCurrentStateName() == "ButtonStatePressed":
            gameObject.FSM.switchState("ButtonStateReleased", ms)
    
            EasyPygame.consume(1)

class Button(GameObject):
    def __init__(self, scene, buttonName="Button", callback=None):
        super().__init__(scene, buttonName)
        self.callback = callback
        self.addInputHandler(ButtonInputHandler())
        self.useInputHandler(1)
        self.addTextureView(DefaultTextureView((255, 0, 0)))
        self.FSM.addState(ButtonStatePressed())
        self.FSM.addState(ButtonStateReleased())

    def setCallback(self, callback):
        self.callback = callback