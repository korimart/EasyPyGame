import EasyPygame

class myApp(EasyPygame.IApp):
    def __init__(self):
        self.imageRect = EasyPygame.Rect(0, 0, 100, 100)
        self.screenRect = EasyPygame.Rect(400, 400, 0, 0)
        EasyPygame.load("abc.jpg")

    def update(self, ms):
        if EasyPygame.isDown("d"):
            print("d is down")

    def render(self, ms):
        EasyPygame.drawImage("abc.jpg", self.imageRect, self.screenRect)


EasyPygame.init(500, 500, "test", 75)
app = myApp()
EasyPygame.run(app)