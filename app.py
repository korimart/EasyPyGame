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
        self.carrot.renderer = EasyPygame.Components.Renderer("abc.jpg")
        self.carrot.inputHandler = carrotHandler()

    def update(self, ms):
        self.scene1.update(ms)

    def render(self, ms):
        self.scene1.render(ms)

if __name__ == "__main__":
    EasyPygame.init(500, 500, "test", 75)
    EasyPygame.run(myApp())