import EasyPygame

class WhiteCarrot(EasyPygame.Components.GameObject):
    def __init__(self):
        super().__init__()
        EasyPygame.load("abc.jpg")
        self.renderer = EasyPygame.Components.Renderer("abc.jpg", 50)

    def handleInput(self, ms):
        if EasyPygame.isDown1stTime("d"):
            self.rect.x += 1
        elif EasyPygame.isDown1stTime("a"):
            self.rect.x -= 1

class myApp(EasyPygame.IApp):
    def __init__(self):
        self.carrot = WhiteCarrot()

    def update(self, ms):
        self.carrot.update(ms)

    def render(self, ms):
        self.carrot.render(ms)

if __name__ == "__main__":
    EasyPygame.init(500, 500, "test", 75)
    EasyPygame.run(myApp())