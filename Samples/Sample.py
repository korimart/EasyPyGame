import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame

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

class Scene1(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()
        self.carrot = None
        self.testObj1 = None
        self.testObj2 = None

    def onLoad(self):
        EasyPygame.load("Carrot.jpg")
        self.carrot = EasyPygame.Components.GameObject(self, "Carrot")
        self.carrot.addTextureView(EasyPygame.Components.TextureView("Carrot.jpg"))
        self.carrot.addTextureView(EasyPygame.Components.DefaultTextureView())
        self.carrot.addInputHandler(carrotHandler())

        # carrot will switch between textureview 0 and 1 when moving left and right
        self.carrot.FSM.addState(EasyPygame.Components.GameObjectState(1, 1))
        self.carrot.FSM.addState(EasyPygame.Components.GameObjectState(1, 2))
        self.carrot.FSM.switchState(2, 0)

        self.testObj1 = EasyPygame.Components.GameObject(self, "Test1")
        self.testObj1.rect.x = 100
        self.testObj1.z = -1
        self.testObj1.addInputHandler(carrotHandler())

        # this will have no effect because testObj1 does not have textureview 1
        self.testObj1.FSM.addState(EasyPygame.Components.GameObjectState(1, 0))
        self.testObj1.FSM.addState(EasyPygame.Components.GameObjectState(1, 1))
        self.testObj1.FSM.switchState(1, 0)

        self.testObj2 = EasyPygame.Components.GameObject(self, "Test2")
        self.testObj2.rect.x = -150
        self.testObj2.rect.y = -150
        self.testObj2.rect.width = 200
        self.testObj2.z = 1

        self.button = EasyPygame.Components.GUI.Button(self, "Button", lambda: self.testCallback())
        self.button.rect.x = 150
        self.button.rect.y = -150

    def preRender(self, ms):
        EasyPygame.pprint("This is Scene1", 0, 0)

    def postRender(self, ms):
        if EasyPygame.isDown1stTime("p"):
            EasyPygame.consume("p")
            EasyPygame.nextScene("Scene1", "Scene2")

    def onUnLoad(self):
        EasyPygame.unload("Carrot.jpg")

    def testCallback(self):
        print("haha")

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

        self.textbox = EasyPygame.Components.GUI.TextBox(self, "textbox1", "Click me to type:")
        self.textbox.rect.x = 0
        self.textbox.rect.y = 100
        self.textbox.rect.width = 400

    def postRender(self, ms):
        EasyPygame.pprint("This is Scene2", 0, 0)

        if EasyPygame.isDown1stTime("p"):
            EasyPygame.consume("p")
            EasyPygame.nextScene("Scene2", "Scene1")

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()
