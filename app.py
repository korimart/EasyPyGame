import EasyPygame

class InnerClass:
    def update(self, ms):
        if EasyPygame.isDown("d"):
            print("d2 is down")

class myApp(EasyPygame.IApp):
    def __init__(self):
        self.imageRect = EasyPygame.Rect(0, 0, 100, 100)
        self.screenRect = EasyPygame.Rect(400, 400, 0, 0)
        self.fontSRect = EasyPygame.Rect(0, 0, 0, 0)
        self.inner = InnerClass()
        EasyPygame.load("abc.jpg")
        EasyPygame.loadFont("Comic Sans MS", 30)
        EasyPygame.createTextImage("Comic Sans MS", 30, (255, 0, 0), "title", "HELLO WORLD!")

    def update(self, ms):
        if EasyPygame.isDown1stTime("d"):
            print("d is down")
        EasyPygame.consume("d") 
        self.inner.update(ms)

    def render(self, ms):
        EasyPygame.drawImage("abc.jpg", self.screenRect, self.imageRect)
        EasyPygame.drawImage("title", self.fontSRect)


EasyPygame.init(500, 500, "test", 75)
app = myApp()
EasyPygame.run(app)