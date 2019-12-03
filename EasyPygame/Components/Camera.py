import EasyPygame

# 좌표계:
# 카메라의 거리가 k일때 x, y 방향으로 [-k, k]만큼 보인다.


class Camera:
    DEFAULTDIST = 3

    def __init__(self, initPos=(0, 0)):
        self.initPos = initPos
        self.transform = EasyPygame.Components.TransformComp(*initPos, self.DEFAULTDIST)
        self.pos = list(initPos)
        self.distance = self.DEFAULTDIST

    def screen2worldCoord(self, screenPos, targetZ=0):
        width = EasyPygame.getWindowWidth()
        height = EasyPygame.getWindowHeight()

        x = screenPos[0] / width * 2 - 1
        y = 1 - screenPos[1] / height * 2
        x *= self.distance - targetZ
        y *= self.distance - targetZ
        x += self.pos[0]
        y += self.pos[1]
        return (x, y)

    def reset(self):
        self.moveTo(*self.initPos)
        self.setDistance(self.DEFAULTDIST)

    def setDistanceDelta(self, delta):
        if (self.distance + delta > 0.3):
            self.distance += delta
            self.transform.translate(0, 0, delta)

    def setDistance(self, distance):
        if (distance > 0.3):
            self.distance = distance
            self.transform.setTranslate(*self.pos, distance)

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
        self.transform.translate(*delta, 0)

    def moveTo(self, x, y):
        self.pos[0] = x
        self.pos[1] = y
        self.transform.setTranslate(*self.pos, self.distance)