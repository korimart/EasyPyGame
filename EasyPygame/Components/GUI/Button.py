import EasyPygame
from EasyPygame.Components import *

class ButtonReleased(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.renderComp = gameObject.releaseRC

    def update(self, gameObject, ms):
        if gameObject.isMouseOn():
            gameObject.switchState(2, ms)

class ButtonPressed(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.renderComp = gameObject.pressRC

    def update(self, gameObject, ms):
        if not EasyPygame.isDown("MOUSELEFT"):
            gameObject.switchState(1, ms)
            gameObject.callback()

class ButtonHover(GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.renderComp = gameObject.hoverRC

    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("MOUSELEFT"):
            EasyPygame.consume("MOUSELEFT")
            gameObject.switchState(3, ms)
        elif not gameObject.isMouseOn():
            gameObject.switchState(1, ms)

class Button(GameObject):
    def __init__(self, scene, name="Button", callback=None):
        super().__init__(scene, name)
        self.transform.setParent(scene.camera.transform)
        self.transform.translate(0, 0, -scene.camera.DEFAULTDIST)
        self.callback = callback
        self.fixedRect = EasyPygame.Rect(0, 0, 1, 1)

        self.releaseRC = DefaultRenderComponent()
        self.pressRC = DefaultRenderComponent((1, 0, 0))
        self.hoverRC = DefaultRenderComponent((0, 1, 0))

        self.addState(ButtonReleased())
        self.addState(ButtonHover())
        self.addState(ButtonPressed())

        self.switchState(1, 0)

    def setCallback(self, callback):
        self.callback = callback

    # def yourLogic(self, ms):
    #     camPos = self.scene.camera.pos
    #     camDist = self.scene.camera.distance
    #     self.setXYZ(camPos[0] + self.fixedRect.x, camPos[1] + self.fixedRect.y, camDist - 3)