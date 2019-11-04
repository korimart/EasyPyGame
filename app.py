import EasyPygame
import pygame

class WhiteCarrot(EasyPygame.Components.GameObject):
    def __init__(self, scene):
        super().__init__(scene)
        EasyPygame.load("abc.jpg")
        self.renderer = EasyPygame.Components.Renderer("abc.jpg")

    def handleInput(self, ms):
        if EasyPygame.isDown1stTime("d"):
            self.rect.x += 100
        elif EasyPygame.isDown1stTime("a"):
            self.rect.x -= 100
        elif EasyPygame.isDown1stTime("w"):
            self.rect.y += 100
        elif EasyPygame.isDown1stTime("s"):
            self.rect.y -= 100

class myApp(EasyPygame.IApp):
    def __init__(self):
        self.scene1 = EasyPygame.Components.Scene(500, 500)
        # self.scene1.camera.moveTo(100, 100)
        self.carrot = WhiteCarrot(self.scene1)

    def update(self, ms):
        self.scene1.update(ms)

    def render(self, ms):
        self.scene1.render(ms)

if __name__ == "__main__":
    EasyPygame.init(500, 500, "test", 75)
    EasyPygame.run(myApp())