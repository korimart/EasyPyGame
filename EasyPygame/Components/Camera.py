class Camera:
    def __init__(self, scene, initPos=[0, 0]):
        self.scene = scene
        self.pos = initPos

    def view(self, pos):
        x = pos[0] - self.pos[0] + self.scene.width / 2
        y = self.pos[1] - pos[1] + self.scene.height / 2
        return (x, y)

    def move(self, delta):
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]

    def moveTo(self, x, y):
        self.pos[0] = x
        self.pos[1] = y