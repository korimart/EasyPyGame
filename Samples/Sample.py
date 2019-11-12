import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame

class wentLeft(EasyPygame.Components.GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(0)

class wentRight(EasyPygame.Components.GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(1)

class carrotHandler(EasyPygame.Components.InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("d"):
            gameObject.rect.x += 100
            gameObject.FSM.switchState(2, ms)
        elif EasyPygame.isDown1stTime("a"):
            gameObject.rect.x -= 100
            gameObject.FSM.switchState(1, ms)
        elif EasyPygame.isDown1stTime("w"):
            gameObject.rect.y += 100
        elif EasyPygame.isDown1stTime("s"):
            gameObject.rect.y -= 100
        elif EasyPygame.isDown1stTime("p"):
            EasyPygame.loadScene("Scene2")
            EasyPygame.switchScene("Scene2")
            EasyPygame.unloadScene("Scene1")

class Scene1(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()
        self.carrot = None
        self.testObj1 = None
        self.testObj2 = None

    def onLoad(self):
        EasyPygame.load("Carrot.jpg")
        self.carrot = EasyPygame.Components.GameObject(self, "Carrot")
        carrotTextureViewIndex = self.carrot.addTextureView(EasyPygame.Components.TextureView("Carrot.jpg"))
        self.carrot.useTextureView(carrotTextureViewIndex)
        self.carrot.addInputHandler(carrotHandler())
        self.carrot.useInputHandler(1)
        # carrot will switch between textureview 0 and 1 when moving left and right
        self.carrot.FSM.addState(wentLeft())
        self.carrot.FSM.addState(wentRight())

        self.testObj1 = EasyPygame.Components.GameObject(self, "Test1")
        self.testObj1.rect.x = 100
        self.testObj1.z = -1
        self.testObj1.addInputHandler(carrotHandler())
        self.testObj1.useInputHandler(1)
        # this will have no effect because testObj1 does not have textureview 1
        self.testObj1.FSM.addState(wentLeft())
        self.testObj1.FSM.addState(wentRight())

        self.testObj2 = EasyPygame.Components.GameObject(self, "Test2")
        self.testObj2.rect.x = -150
        self.testObj2.rect.y = -150
        self.testObj2.rect.width = 200
        self.testObj2.z = 1

        self.button = EasyPygame.Components.GUI.Button(self, "Button", lambda: self.testCallback())
        self.button.rect.x = 150
        self.button.rect.y = -150

        self.textbox = EasyPygame.Components.GUI.TextBox(self)
        self.textbox.rect.x = 150
        self.textbox.rect.y = 200

    def preRender(self):
        EasyPygame.pprint("preRender preRender preRender", 0, 0)

    def postRender(self):
        EasyPygame.pprint("postRender postRender postRender", 0, 100)

    def unload(self):
        EasyPygame.unload("Carrot.jpg")

    def testCallback(self):
        print(self.textbox.getText())

class Scene2(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()

    def onLoad(self):
        self.obj1 = EasyPygame.Components.GameObject(self, "obj1")
        self.obj1.addTextureView(EasyPygame.Components.DefaultTextureView((255, 0, 0)))
        # first parameter is gameObjectStateIndex to attach AnimationState to.
        # second parameter is an AnimationState
        # first parameter of the constructor is duration in miliseconds of the animation from start to end
        # second parameter is a list of textureViewIndices of animation
        # in this case, animates between textureView 0 and 1 each with duration of 0.5 seconds and total of 1 second
        self.obj1.FSM.attachAnimationState(0, EasyPygame.Components.SpriteAnimState(1000, [0, 1]))

    def postRender(self):
        EasyPygame.pprint("this is scene2", 0, 0)

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()
