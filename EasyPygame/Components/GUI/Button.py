import EasyPygame
from EasyPygame.Components import *

class ButtonReleased(GameObjectState):
    def update(self, gameObject, ms):
        if gameObject.isMouseOn():
            gameObject.FSM.switchState(2, ms)

class ButtonPressed(GameObjectState):
    def update(self, gameObject, ms):
        if not EasyPygame.isDown("MOUSELEFT"):
            gameObject.FSM.switchState(1, ms)
            gameObject.callback()

class ButtonHover(GameObjectState):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("MOUSELEFT"):
            EasyPygame.consume("MOUSELEFT")
            gameObject.FSM.switchState(3, ms)
        elif not gameObject.isMouseOn():
            gameObject.FSM.switchState(1, ms)

class Button(GameObject):
    def __init__(self, scene, name="Button", callback=None):
        super().__init__(scene, name)
        self.callback = callback

        # texture views: 1, 2, 3
        self.addTextureView(DefaultTextureView((0, 0, 255)))
        self.addTextureView(DefaultTextureView((0, 255, 0)))
        self.addTextureView(DefaultTextureView((255, 0, 0)))

        self.FSM.addState(ButtonReleased())
        self.FSM.addState(ButtonHover())
        self.FSM.addState(ButtonPressed())
        self.FSM.attachConcurrentState(1, StaticTextureState(1))
        self.FSM.attachConcurrentState(2, StaticTextureState(2))
        self.FSM.attachConcurrentState(3, StaticTextureState(3))

        self.FSM.switchState(1, 0)

    def setCallback(self, callback):
        self.callback = callback