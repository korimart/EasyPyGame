import glm

class TransformComp:
    def __init__(self, x=0, y=0, z=0, parent=None):
        self.parent = parent
        self.worldMat = glm.translate(glm.mat4(), glm.vec3(x, y, z))

    def reset(self):
        self.worldMat = glm.mat4()

    def getWorldMat(self):
        ret = glm.mat4()
        if self.parent:
            ret = parent.getWorldMat()

        return ret * self.worldMat

    def translate(self, x, y, z):
        self.worldMat = glm.translate(self.worldMat, glm.vec3(x, y, z))

    def rotate(self, angle):
        self.worldMat = glm.rotate(self.worldMat, glm.radians(angle), glm.vec3(0, 0, 1))

    def scale(self, x, y):
        self.worldMat = glm.scale(self.worldMat, glm.vec3(x, y, 1))

    def copy(self):
        new = TransformComp()
        new.parent = self.parent
        new.worldMat = glm.mat4(self.worldMat)
        return new