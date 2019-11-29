from EasyPygame.Components import *

class Terrain:
    NOTHING = 0
    HAZARD = 1
    BLOB = 2

class Floor(GameObject):
    def __init__(self, scene, width, height):
        super().__init__(scene, "Floor")
        self.terrain = []
        self.uncovered = []
        self.width = width
        self.height = height
        self.mazeGenerator = None

        self.wall = GameObject(scene, "Wall")
        # self.wall.addTextureView(InstancedTextureView())

    def randomize(self):
        self.terrain = self.mazeGenerator.generate(self.width, self.height)
        self.uncovered = [[0 for _ in range(width)] for _ in range(height)]

    def restart(self, map):
        pass

    def senseBlob(self, x, y):
        ret = self.terrain[x][y]
        if ret == Terrain.BLOB:
            self.uncovered[x][y] = Terrain.BLOB
            return True

        return False

    def senseHazard(self, x, y):
        ret = self.terrain[x][y]
        if ret == Terrain.HAZARD:
            self.uncovered[x][y] = Terrain.HAZARD
            return True

        return False