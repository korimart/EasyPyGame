import EasyPygame

class Camera:
    def __init__(self, initPos=[0, 0]):
        self.pos = initPos
        self.distance = 1

    def view(self, pos):
        x = pos[0] - self.pos[0] + EasyPygame.getWindowWidth() / 2
        y = self.pos[1] - pos[1] + EasyPygame.getWindowHeight() / 2
        return (x, y)
    
    def realView(self, pos):
        x = pos[0] - self.pos[0]
        y = pos[1] - self.pos[1]
        return (x, y)

    def unview(self, pos):
        x = pos[0] + self.pos[0] - EasyPygame.getWindowWidth() / 2
        y = self.pos[1] + EasyPygame.getWindowHeight() / 2 - pos[1]
        return (x, y)

    def move(self, delta):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]

    def moveTo(self, x, y):
        self.pos[0] = x
        self.pos[1] = y