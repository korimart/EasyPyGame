import EasyPygame
from EasyPygame.Components import *
from SimApp.MazeGenerator import *

class Floor(GameObject):
    def __init__(self, scene, width, height):
        super().__init__(scene, "Floor")
        self.terrain = []
        self.uncovered = []
        self.width = width
        self.height = height
        self.mazeGenerator = MazeGenerator()

        self.wall = GameObject(scene, "Wall")
        self.wall.uncoveredRects = []
        imageRect = EasyPygame.Rect(32 / 512, 12 / 512, 16 / 512, 16 / 512)
        self.wall.addTextureView(InstancedTextureView("animated.png", self.wall.uncoveredRects, imageRect))
        self.wall.useTextureView(1)

    def randomize(self, targetList):
        self.terrain = self.mazeGenerator.generate(self.width, self.height, targetList)
        self.uncovered = [[0 for _ in range(self.width)] for _ in range(self.height)]
        # test
        for i in range(self.height):
            for j in range(self.width):
                if self.terrain[i][j]:
                    self._uncover(j, i)

    def restart(self, map):
        pass

    def senseBlob(self, x, y):
        ret = self.terrain[x][y]
        if ret == Terrain.BLOB:
            self.uncovered[x][y] = Terrain.BLOB
            self._uncover(x, y)
            return True

        return False

    def senseHazard(self, x, y):
        ret = self.terrain[x][y]
        if ret == Terrain.HAZARD:
            self.uncovered[x][y] = Terrain.HAZARD
            self._uncover(x, y)
            return True

        return False

    def _uncover(self, x, y):
        rt = EasyPygame.EasyPygameRect(x, y, 1, 1)
        self.wall.uncoveredRects.append(rt)
