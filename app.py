import EasyPygame

class myApp(EasyPygame.IApp):
    def __init__(self):
        self.x = 0
        self.transform = 50
        self.screenRect = EasyPygame.Rect(self.x, 150, 0, 0)
        self.animationProgress = 0
        self.animationState = False
        EasyPygame.load("abc.jpg")

    def update(self, ms):
        # input handler
        if EasyPygame.isDown1stTime("d"):
            self.x += 1
            self.animationState = True
        elif EasyPygame.isDown1stTime("a"):
            self.x -= 1

    def render(self, ms):
        # render
        if self.animationState:
            if self.animationProgress <= 500:
                self.screenRect.x = (self.animationProgress / 500 + self.x - 1) * self.transform
                self.animationProgress += ms
            else:
                self.animationProgress = 0
                self.animationState = False
        else:
            self.screenRect.x = self.x * self.transform
        EasyPygame.drawImage("abc.jpg", self.screenRect)

if __name__ == "__main__":
    EasyPygame.init(500, 500, "test", 75)
    EasyPygame.run(myApp())