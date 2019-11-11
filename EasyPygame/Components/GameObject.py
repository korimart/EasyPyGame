import EasyPygame
from EasyPygame.Components import TextureView
from EasyPygame.Components import InputHandler
from EasyPygame.Components import FSM

class GameObject:
    def __init__(self, scene, name="GameObject"):
        self.rect = EasyPygame.Rect(0, 0, 100, 100)

        self.textureViewList = [TextureView.DefaultTextureView()]
        self.inputHandlerList = [InputHandler.InputHandler()]
        self.FSM = FSM.FSM(self)
        self.textureViewIndex = 0
        self.inputHandlerIndex = 0

        self.scene = scene
        self.name = name
        self.z = 0
        scene.addGameObject(self)

    def update(self, ms):
        self.inputHandlerList[self.inputHandlerIndex].update(self, ms)
        self.yourLogic(ms)

    def yourLogic(self, ms):
        pass

    def render(self, ms):
        self.textureViewList[self.textureViewIndex].render(self, self.scene.camera)

    def addTextureView(self, textureView):
        self.textureViewList.append(textureView)
        return len(self.textureViewList) - 1

    def addInputHandler(self, inputHandler):
        self.inputHandlerList.append(inputHandler)
        return len(self.inputHandlerList) - 1

    def useTextureView(self, textureViewIndex):
        if 0 <= textureViewIndex < len(self.textureViewList):
            self.textureViewIndex = textureViewIndex
        else:
            self.textureViewIndex = 0

    def useInputHandler(self, inputHandlerIndex):
        if 0 <= inputHandlerIndex < len(self.inputHandlerList):
            self.inputHandlerIndex = inputHandlerIndex
        else:
            self.inputHandlerIndex = 0

    def __eq__(self, other):
        return self.z == other.z

    def __lt__(self, other):
        return self.z < other.z