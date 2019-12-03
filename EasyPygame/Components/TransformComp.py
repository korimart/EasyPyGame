import glm

coords = [
    0.5, 0.5,
    0.5, -0.5,
    -0.5, 0.5,
    -0.5, -0.5
]

class TransformComp:
    def __init__(self, x=0, y=0, z=0, parent=None):
        self.parent = parent
        self.worldMat = glm.translate(glm.mat4(), glm.vec3(x, y, z))

    def reset(self):
        self.worldMat = glm.mat4()

    def getWorldMat(self):
        ret = glm.mat4()
        if self.parent:
            ret = self.parent.getWorldMat()

        return ret * self.worldMat

    def translate(self, x, y, z):
        self.worldMat = glm.translate(self.worldMat, glm.vec3(x, y, z))

    def setTranslate(self, x, y, z):
        self.worldMat = glm.translate(glm.mat4(), glm.vec3(x, y, z))

    def rotate(self, angle):
        self.worldMat = glm.rotate(self.worldMat, glm.radians(angle), glm.vec3(0, 0, 1))

    def scale(self, x, y):
        self.worldMat = glm.scale(self.worldMat, glm.vec3(x, y, 1))

    def copy(self):
        new = TransformComp()
        new.parent = self.parent
        new.worldMat = glm.mat4(self.worldMat)
        return new

    def setParent(self, parent):
        self.parent = parent

    def getZ(self):
        return (self.getWorldMat() * glm.vec4(0, 0, 0, 1))[2]

    def collidepoint(self, x, y):
        points = []
        world = self.getWorldMat()
        for i in range(4):
            points.append(world * glm.vec4(coords[i * 2], coords[i * 2 + 1], 0, 1))

        xes, ys = [], []
        for point in points:
            xes.append(point[0])
            ys.append(point[1])

        xMin, xMax, yMin, yMax = min(xes), max(xes), min(ys), max(ys)
        return xMin <= x <= xMax and yMin <= y <= yMax