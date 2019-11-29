import EasyPygame
from EasyPygame.Components import TextureView
from EasyPygame.Components import FSM

class GameObject:
    def __init__(self, scene, name="GameObject"):
        self.rect = EasyPygame.Rect(0, 0, 1, 1)

        self.textureViewList = [TextureView.InvisibleTextureView()]
        self.FSM = FSM.FSM(self)
        self.textureViewIndex = 0

        self.scene = scene
        self.name = name
        scene.addGameObject(self)

    def update(self, ms):
        self.FSM.update(ms)

    def yourLogic(self, ms):
        pass

    def render(self, ms):
        self.textureViewList[self.textureViewIndex].render(self)

    def addTextureView(self, textureView):
        self.textureViewList.append(textureView)
        return len(self.textureViewList) - 1

    def useTextureView(self, textureViewIndex):
        if 0 <= textureViewIndex < len(self.textureViewList):
            self.textureViewIndex = textureViewIndex
        else:
            self.textureViewIndex = 0

    def disable(self):
        self.useTextureView(0)
        self.FSM.switchState(0, 0)

    def enable(self, stateIndex):
        self.FSM.switchState(stateIndex, 0)

    def isMouseOn(self):
        camera = self.scene.camera
        mousePos = EasyPygame.getMousePos()
        x, y = camera.screen2worldCoord(mousePos)
        try:
            return self.rect.collidepoint(x, y)
        except AttributeError:
            return False

    def __eq__(self, other):
        return self.rect.z == other.rect.z

    def __lt__(self, other):
        return self.rect.z < other.rect.z