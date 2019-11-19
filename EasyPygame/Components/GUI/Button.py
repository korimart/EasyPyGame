import EasyPygame
from EasyPygame.Components import GameObject
from EasyPygame.Components import InputHandler
from EasyPygame.Components import DefaultTextureView, InvisibleTextureView
from EasyPygame.Components import GameObjectState

class ButtonInputHandlerReleased(InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isMouseOnObject(gameObject):
            gameObject.FSM.switchState(2, ms)

class ButtonInputHandlerPressed(InputHandler):
    def update(self, gameObject, ms):
        if not EasyPygame.isDown("MOUSELEFT"):
            gameObject.FSM.switchState(1, ms)

class ButtonInputHandlerHover(InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("MOUSELEFT"):
            EasyPygame.consume("MOUSELEFT")
            gameObject.FSM.switchState(3, ms)
            gameObject.callback()
        elif not EasyPygame.isMouseOnObject(gameObject):
            gameObject.FSM.switchState(1, ms)

class Button(GameObject):
    def __init__(self, scene, name="Button", callback=None):
        super().__init__(scene, name)
        self.callback = callback

        # handlers: 1, 2, 3
        self.addInputHandler(ButtonInputHandlerReleased())
        self.addInputHandler(ButtonInputHandlerHover())
        self.addInputHandler(ButtonInputHandlerPressed())

        # texture views: 1, 2, 3
        self.addTextureView(DefaultTextureView((0, 0, 255)))
        self.addTextureView(DefaultTextureView((0, 255, 0)))
        self.addTextureView(DefaultTextureView((255, 0, 0)))

        self.FSM.addState(GameObjectState(1, 1))
        self.FSM.addState(GameObjectState(2, 2))
        self.FSM.addState(GameObjectState(3, 3))
        self.FSM.switchState(1, 0)

    def setCallback(self, callback):
        self.callback = callback