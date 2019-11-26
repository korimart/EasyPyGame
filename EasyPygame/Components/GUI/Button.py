import EasyPygame
from EasyPygame.Components import GameObject
from EasyPygame.Components import DefaultTextureView, InvisibleTextureView, StaticTextureState
from EasyPygame.Components import GameObjectState

class ButtonReleased(StaticTextureState):
    def update(self, gameObject, ms):
        if gameObject.isMouseOn():
            gameObject.FSM.switchState(2, ms)

class ButtonPressed(StaticTextureState):
    def update(self, gameObject, ms):
        if not EasyPygame.isDown("MOUSELEFT"):
            gameObject.FSM.switchState(1, ms)

class ButtonHover(StaticTextureState):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("MOUSELEFT"):
            EasyPygame.consume("MOUSELEFT")
            gameObject.FSM.switchState(3, ms)
            gameObject.callback()
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

        self.FSM.addState(ButtonReleased(1))
        self.FSM.addState(ButtonHover(2))
        self.FSM.addState(ButtonPressed(3))
        self.FSM.switchState(1, 0)

    def setCallback(self, callback):
        self.callback = callback