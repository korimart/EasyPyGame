import EasyPygame

class WhiteCarrot(EasyPygame.Components.GameObject):
    class HandleCarrot(EasyPygame.Components.InputHandler):
        def __init__(self):
            super().__init__()

        def update(self, gameObject):
            if EasyPygame.isDown1stTime("d"):
                gameObject.screenRect.x += 1
            elif EasyPygame.isDown1stTime("a"):
                gameObject.screenRect.x -= 1

    def __init__(self):
        super().__init__(self.HandleCarrot(), EasyPygame.Components.Renderer("abc.jpg", 50))
        self.screenRect = EasyPygame.Rect(0, 150, 0, 0)
        EasyPygame.load("abc.jpg")

class myApp(EasyPygame.IApp):
    def __init__(self):
        # self.x = 0
        # self.transform = 50
        # self.screenRect = EasyPygame.Rect(self.x, 150, 0, 0)
        # self.animationProgress = 0
        # self.animationState = False
        # EasyPygame.load("abc.jpg")
        self.carrot = WhiteCarrot()

    def update(self, ms):
        # # input handler
        # if EasyPygame.isDown1stTime("d"):
        #     self.x += 1
        #     self.animationState = True
        # elif EasyPygame.isDown1stTime("a"):
        #     self.x -= 1
        self.carrot.update(ms)

    def render(self, ms):
        # # render
        # if self.animationState:
        #     if self.animationProgress <= 500:
        #         self.screenRect.x = (self.animationProgress / 500 + self.x - 1) * self.transform
        #         self.animationProgress += ms
        #     else:
        #         self.animationProgress = 0
        #         self.animationState = False
        # else:
        #     self.screenRect.x = self.x * self.transform
        # EasyPygame.drawImage("abc.jpg", self.screenRect)
        self.carrot.render(ms)

if __name__ == "__main__":
    EasyPygame.init(500, 500, "test", 75)
    EasyPygame.run(myApp())