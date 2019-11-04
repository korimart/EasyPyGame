import EasyPygame

class carrotHandler(EasyPygame.Components.InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("d"):
            gameObject.rect.x += 100
        elif EasyPygame.isDown1stTime("a"):
            gameObject.rect.x -= 100
        elif EasyPygame.isDown1stTime("w"):
            gameObject.rect.y += 100
        elif EasyPygame.isDown1stTime("s"):
            gameObject.rect.y -= 100

class myApp(EasyPygame.IApp):
    def __init__(self):
        EasyPygame.load("abc.jpg")

        self.scene1 = EasyPygame.Components.Scene(500, 500)

        self.carrot = EasyPygame.Components.GameObject(self.scene1, "Carrot")
        self.carrot.textureView = EasyPygame.Components.TextureView("abc.jpg")
        self.carrot.inputHandler = carrotHandler()

        self.testObj1 = EasyPygame.Components.GameObject(self.scene1, "Test1")
        self.testObj1.rect.x = 100
        self.testObj1.z = -1

        self.testObj2 = EasyPygame.Components.GameObject(self.scene1, "Test2")
        self.testObj2.rect.x = -100
        self.testObj2.rect.y = 100
        self.testObj2.rect.width = 200
        self.testObj2.z = 1

        # EasyPygame.unload("abc.jpg")

    def update(self, ms):
        self.scene1.update(ms)

    def render(self, ms):
        self.scene1.render(ms)
        EasyPygame.pprint("This is a sample program!", 0, 0)

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.run(myApp())