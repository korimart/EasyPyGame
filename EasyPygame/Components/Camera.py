import EasyPygame

# 좌표계:
# 카메라의 거리가 k일때 x, y 방향으로 [-k, k]만큼 보인다.

class Camera:
    def __init__(self, initPos=[0, 0]):
        self.pos = initPos
        self.distance = 3

    def screen2worldCoord(self, screenPos):
        width = EasyPygame.getWindowWidth()
        height = EasyPygame.getWindowHeight()

        x = screenPos[0] / width * 2 - 1
        y = 1 - screenPos[1] / height * 2
        x *= self.distance
        y *= self.distance
        x += self.pos[0]
        y += self.pos[1]
        return (x, y)

    def reset(self):
        self.moveTo(0, 0)
        self.distance = 3

    def setDistanceDelta(self, delta):
        if (self.distance + delta > 0.3):
            self.distance += delta

    def setDistance(self, distance):
        if (distance > 0.3):
            self.distance = distance

    def view(self, pos):
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